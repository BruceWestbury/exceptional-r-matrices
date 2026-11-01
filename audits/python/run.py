#!/usr/bin/env python3
"""Linux process-isolated benchmark with fixed hard time budgets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
ORDER = [(5, 'X3', 1), (6, 'Y3', 1), (7, 'Y3_star', 1),
         (9, 'C', 2), (10, 'C_star', 2), (8, 'A', 3), (0, 'I', 5),
         (3, 'Y2', 6), (4, 'Y2_star', 6), (2, 'X2', 7), (1, 'L', 11)]


def worker(index, path, limit):
    os.setsid()
    # Kernel timer enforces the whole worker budget, including imports.
    signal.signal(signal.SIGALRM, lambda *_: os.killpg(os.getpgrp(), signal.SIGKILL))
    signal.setitimer(signal.ITIMER_REAL, limit)
    with path.open('x') as log:
        def emit(record):
            log.write(json.dumps(record) + '\n')
            log.flush()
        try:
            import flint
            flint.ctx.threads = 1
            from spectral_ybe import audit
            result = audit(index, emit)
            code = 0 if result['status'] == 'PASS' else 1
        except BaseException:
            emit({'status': 'ERROR', 'traceback': traceback.format_exc()})
            code = 2
    os._exit(code)


def provenance():
    import flint
    inputs = [ROOT / 'data/dilute_a3.json', ROOT / 'data/local_a2.json',
              ROOT / 'reports/paper_audit/local_embeddings.json']
    for index, _, _ in ORDER:
        inputs.extend([ROOT / f'data/dilute_representations/Dilute_{index}.json',
                       ROOT / f'reports/paper_audit/spectral_{index}.json'])
    inputs.extend([ROOT / 'audits/python/spectral_ybe.py', ROOT / 'audits/python/run.py'])
    return {'python': platform.python_version(), 'python_flint': flint.__version__,
            'flint': flint.__FLINT_VERSION__, 'platform': platform.platform(),
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in inputs}}


def render(results, c_results, output):
    c_by_index = {r['index']: r for r in c_results['results']}
    comparisons = []
    for row in results:
        c = c_by_index[row['index']]
        comparisons.append({'index': row['index'], 'python_status': row['status'],
                            'C_status': c['status'], 'C_wall_seconds': c['wall_seconds'],
                            'status_agreement': row['status'] == c['status']})
    (output / 'comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    lines = ['# Independent Python/FLINT spectral YBE audit', '',
             'Exact arithmetic over QQ(p,q,u,v), with algebraically independent variables.', '',
             '| Representation | Dim. | Python | C | Construct s | YBE s | Compare s | Wall s | Peak MiB |',
             '|---|---:|---|---|---:|---:|---:|---:|---:|']
    for row, comparison in zip(results, comparisons):
        def timing(key):
            value = row.get(key)
            return '—' if value is None else f'{value:.4f}'
        lines.append(f"| {row['name']} | {row['dimension']} | {row['status']} | "
                     f"{comparison['C_status']} | {timing('construction_seconds')} | "
                     f"{timing('ybe_seconds')} | {timing('comparison_seconds')} | "
                     f"{timing('wall_seconds')} | {row.get('peak_rss_kib', 0)/1024:.2f} |")
    all_pass = all(r['status'] == 'PASS' for r in results)
    lines += ['', ('All eleven generic symbolic YBE checks and all polynomial/rational comparisons '
                    'PASS with exact zero residuals.' if all_pass else
                   'This batch requires follow-up for the representations listed below.'),
              '', f"Sum of worker wall times: {sum(r.get('wall_seconds', 0) for r in results):.4f} seconds.",
              'Limits: 60 seconds per worker and 300 seconds per batch.', '',
              'Construction uses literal rational equation (8.3), followed by the paper’s polynomial '
              'normalization. Clearing time is separate in results.json. YBE time includes FLINT '
              'composition, both triple products, and every entrywise difference. Comparison occurs '
              'after YBE. Wall time includes interpreter/library import and reporting overhead; '
              'peak RSS is wait4 ru_maxrss on Linux.', '',
              'The Python workers construct and evaluate their own matrices. The report loads C results '
              'after the Python batch finishes. The implementations share the JSON mathematical '
              'specifications and the FLINT library family.', '',
              'The conclusion concerns the supplied representations with the specified embeddings '
              'and normalization. The paper provides the categorical interpretation and abstract '
              'presentation arguments.']
    for row in results:
        if row['status'] != 'PASS':
            lines += ['', f"Follow-up: {row['name']} — {row['status']}; last phase "
                      f"{row.get('last_phase', 'none')}. See rep_{row['index']}.jsonl."]
    (output / 'REPORT.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'audits/python/results')
    parser.add_argument('--batch-seconds', type=float, default=300,
                        help='May reduce, never increase, the 300-second batch limit')
    args = parser.parse_args()
    if not 0 < args.batch_seconds <= 300:
        parser.error('batch-seconds must be positive and at most 300')
    args.output.mkdir(parents=True, exist_ok=False)
    # Dependency inspection and file hashes are outside the mathematical batch.
    metadata = provenance()
    (args.output / 'provenance.json').write_text(json.dumps(metadata, indent=2) + '\n')
    results = []
    batch_start = time.monotonic()
    deadline = batch_start + args.batch_seconds
    for index, name, dimension in ORDER:
        started = time.monotonic()
        budget = min(60, deadline - started)
        row = {'index': index, 'name': name, 'dimension': dimension,
               'effective_limit_seconds': max(0, budget)}
        if budget <= 0:
            row.update(status='NOT ATTEMPTED', reason='batch deadline exhausted', wall_seconds=0)
            results.append(row)
            continue
        path = args.output / f'rep_{index}.jsonl'
        pid = os.fork()
        if pid == 0:
            worker(index, path, budget)
        timed_out = False
        while True:
            found, status, usage = os.wait4(pid, os.WNOHANG)
            if found:
                break
            if time.monotonic() >= started + budget:
                timed_out = True
                try:
                    os.killpg(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                found, status, usage = os.wait4(pid, 0)
                break
            time.sleep(0.005)
        elapsed = time.monotonic() - started
        records = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        for record in records:
            if 'phase' in record:
                row['last_phase'] = record['phase']
            row.update({k: v for k, v in record.items() if k.endswith('_seconds')})
        final = next((r for r in reversed(records) if 'status' in r), {})
        row.update(final)
        signaled = os.WIFSIGNALED(status)
        killed_at_deadline = signaled and os.WTERMSIG(status) == signal.SIGKILL and elapsed >= budget - 0.05
        if timed_out or killed_at_deadline:
            row['status'] = 'TIMEOUT'
        elif signaled or not final:
            row['status'] = 'ERROR'
        row.update(wall_seconds=elapsed, peak_rss_kib=usage.ru_maxrss,
                   process_exit=os.waitstatus_to_exitcode(status))
        results.append(row)
        print(f"{name}: {row['status']} {elapsed:.3f}s {usage.ru_maxrss/1024:.2f} MiB", flush=True)
    batch_seconds = time.monotonic() - batch_start
    result_document = {'limits_seconds': {'per_representation': 60, 'batch': args.batch_seconds},
                       'batch_wall_seconds': batch_seconds, 'results': results}
    (args.output / 'results.json').write_text(json.dumps(result_document, indent=2) + '\n')
    # Deliberately deferred: no C evidence is consulted before this point.
    c_path = ROOT / 'benchmarks/flint_ybe/results.json'
    c_results = json.loads(c_path.read_text())
    (args.output / 'C_comparison_provenance.json').write_text(json.dumps({
        'path': str(c_path.relative_to(ROOT)), 'sha256': hashlib.sha256(c_path.read_bytes()).hexdigest(),
        'comparison_after_python_batch': True}, indent=2) + '\n')
    render(results, c_results, args.output)


if __name__ == '__main__':
    main()
