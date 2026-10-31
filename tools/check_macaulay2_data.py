#!/usr/bin/env python3
"""Compare the bundled package with JSON over QQ(p,q,u), without changing either.

Python reads the portable scalar grammar; Macaulay2 performs all arithmetic.
Each worker has a 60-second deadline. Data, each package normalization, and
installation have separate 300-second batch deadlines.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
from validate_data import parse_scalar

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['I', 'L', 'X2', 'Y2', 'Y2_star', 'X3', 'Y3', 'Y3_star', 'A', 'C', 'C_star']
DONE = 'EXCEPTIONAL_CHECK_COMPLETE'


def quote(value):
    """M2 strings use the same escapes needed here as JSON strings."""
    return json.dumps(str(value), ensure_ascii=False)


class Scalars:
    """Translate the restricted JSON grammar, never arbitrary source strings."""
    def __init__(self, definitions):
        self.definitions = definitions
        self.names = {s: s for s in ('p', 'q', 'u')}
        self.lines = []
        self.active = set()

    def name(self, name):
        if name in self.names:
            return self.names[name]
        if name in self.active:
            raise ValueError('cyclic coefficient: ' + name)
        if name not in self.definitions:
            raise ValueError('unknown coefficient: ' + name)
        self.active.add(name)
        expression = self.expression(self.definitions[name]['expression'])
        symbol = 'edCoefficient' + str(len(self.names))
        self.names[name] = symbol
        self.lines.append(f'{symbol} = {expression};')
        self.active.remove(name)
        return symbol

    def expression(self, text):
        def emit(node):
            op = node[0]
            if op == 'int':
                return f'({node[1]}_F)'
            if op == 'id':
                return self.name(node[1])
            a = emit(node[1])
            if op == 'neg':
                return f'(-{a})'
            if op == 'pow':
                return f'({a}^({node[2]}))'
            return f'({a}{op}{emit(node[2])})'
        return emit(parse_scalar(text))

    def matrix(self, spec):
        rows = [['0_F'] * spec['cols'] for _ in range(spec['rows'])]
        seen = set()
        for i, j, value in spec['entries']:
            if not (0 <= i < spec['rows'] and 0 <= j < spec['cols']) or (i, j) in seen:
                raise ValueError('invalid matrix coordinate: ' + spec['operator'])
            seen.add((i, j))
            rows[i][j] = self.expression(value)
        return 'matrix {' + ','.join('{' + ','.join(row) + '}' for row in rows) + '}'


COMPARE = r'''
edFailures = 0;
edCompare = (label,actual,expected) -> (
    if numRows actual != numRows expected or numColumns actual != numColumns expected then (
        print("EDFAIL|"|label|"|dimension mismatch"); edFailures=edFailures+1;
    ) else (
        good := true;
        scan(numRows expected,i->scan(numColumns expected,j->(
            if actual_(i,j) != expected_(i,j) then (
                good=false;
                print("EDFAIL|"|label|"|"|toString i|"|"|toString j|
                    "|actual="|toString actual_(i,j)|"|expected="|toString expected_(i,j));
            );
        )));
        if good then print("EDPASS|"|label) else edFailures=edFailures+1;
    );
    flush stdio;
);
'''


def setup(package, configuration):
    return f'''
path = prepend({quote(str(package.parent) + '/')},path);
loadPackage("ExceptionalDiagrams", FileName=>{quote(package)},
    Configuration=>{{"alpha"=>{quote(configuration)},"parameters"=>"generic"}});
debug ExceptionalDiagrams;
assert((options ExceptionalDiagrams).Configuration#"alpha"=={quote(configuration)});
'''


def comparison_program(data, package, index, configuration):
    def read(name):
        return json.loads((data / name).read_text())
    local, algebra = read('local_a2.json'), read('a3.json')
    registry, registry2 = read('dilute_a3.json'), read('dilute_a2.json')
    formula = read('spectral_r.json')
    defs = {**local['coefficients'], **algebra['coefficients'],
            **formula['coefficient_definitions'],
            **{k: {'expression': registry['normalization_prescriptions'][k]}
               for k in ('alpha', 'beta')}}
    spectral = read(f'spectral/Dilute_{index}.json')
    defs.update(spectral['coefficient_definitions'])
    scalars = Scalars(defs)
    lines, labels = [], []
    matrix_count = 0

    def compare(label, actual, expected, matrix=True):
        nonlocal matrix_count
        labels.append(label)
        matrix_count += int(matrix)
        lines.append(f'edCompare({quote(label)},{actual},{expected});')

    if configuration == 'paper':
        for m in read(f'representations/{NAMES[index]}.json')['matrices']:
            op = m['operator']
            generator = op[:-1]
            actual = ('bar(braid())' if generator == 'Sinv' else
                      'braid()' if generator == 'S' else f'diagram {generator}')
            compare('ordinary/' + op,
                    f'rep({index},({actual})_{op[-1]},Dilute=>false)', scalars.matrix(m))

    for reg, doc, strands in [
        (registry, read(f'dilute_representations/Dilute_{index}.json'), 3),
        *(([(registry2, read(f'dilute_a2_representations/{NAMES[index]}.json'), 2)])
          if index < 5 else []),
    ]:
        if len(reg['generators']) != len(doc['matrices']):
            raise ValueError('generator count mismatch')
        for g, m in zip(reg['generators'], doc['matrices']):
            if g['operator'] != m['operator']:
                raise ValueError('generator order mismatch')
            j = g['source_index']
            diagram = f'lst33#{g["source_basis_index"]}' if strands == 3 else f'lst2#{j}'
            multiplier = scalars.expression(g[configuration + '_multiplier'])
            label = f'dilute_A{strands}/' + m['operator']
            # Check the registry's rescaling against the package's geometric rule.
            compare(label + '/scale', f'matrix {{{{(scale({diagram}))^(-1)}}}}',
                    f'matrix {{{{{multiplier}}}}}', matrix=False)
            compare(label, f'rep({index},{diagram},Dilute=>true)',
                    f'({multiplier})*({scalars.matrix(m)})')

    if configuration == 'paper2':
        # Independent spelling of the paper's polynomial prefactor using M2 brackets.
        factor = '(bracket{6,0,0,0})^2*(bracket{1,0,0,0})/((bracket{3,0,0,0})^2*(bracket{2,0,0,0}))*(bracket{1,1,1,0})*(bracket{0,-1,1,0})*(bracket{2,0,1,0})*(bracket{3,0,1,0})'
        compare('spectral/prefactor', f'matrix {{{{{factor}}}}}',
                'matrix {{' + scalars.expression(formula['scalar_relationship']['normalization_scalar']) + '}}',
                matrix=False)
        for m in spectral['matrices']:
            compare('spectral/' + m['operator'],
                    f'({factor})*rep({index},(Rmatrix())_{m["position"]},Dilute=>true)',
                    scalars.matrix(m))
    ending = f'if edFailures>0 then exit 1;\nprint {quote(DONE)};\nexit 0;\n'
    program = setup(package, configuration) + COMPARE + '\n'.join(scalars.lines + lines) + '\n' + ending
    return program, labels, matrix_count


class Runner:
    def __init__(self, m2, scratch):
        self.m2, self.scratch = m2, scratch
        self.started = time.monotonic()
        self.batch_started, self.batch = self.started, 'data'
        self.stages = []

    def begin_batch(self, name):
        self.batch_started, self.batch = time.monotonic(), name

    def run(self, name, program=None, command=None, labels=None, matrices=0):
        seconds = min(60, 300 - (time.monotonic() - self.batch_started))
        if seconds <= 0:
            raise RuntimeError('300-second batch deadline exhausted')
        if program is not None:
            script = self.scratch / (name + '.m2')
            script.write_text(program)
            command = [self.m2, '--script', str(script)]
        started = time.monotonic()
        process = subprocess.Popen(command, cwd=self.scratch, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, start_new_session=True)
        expired = False
        try:
            output, _ = process.communicate(timeout=seconds)
        except subprocess.TimeoutExpired:
            expired = True
            os.killpg(process.pid, signal.SIGKILL)
            output, _ = process.communicate()
        passes = [s.removeprefix('EDPASS|') for s in output.splitlines() if s.startswith('EDPASS|')]
        diagnostics = [s for s in output.splitlines() if s.startswith('EDFAIL|')]
        complete = DONE in output.splitlines() if program is not None else True
        passed = not expired and process.returncode == 0 and complete and not diagnostics
        if labels is not None:
            passed = passed and passes == labels
        stage = {'stage': name, 'batch': self.batch, 'status': 'PASS' if passed else 'TIMEOUT' if expired else 'FAIL',
                 'exit_code': process.returncode, 'seconds': round(time.monotonic() - started, 3),
                 'matrix_comparisons': sum(not s.endswith(('/scale', '/prefactor')) for s in passes),
                 'matrix_comparisons_expected': matrices, 'checks_passed': len(passes)}
        self.stages.append(stage)
        print(name + ': ' + stage['status'], flush=True)
        if not passed:
            stage['diagnostics'] = diagnostics or [output[-8000:]]
            raise RuntimeError(name + ' failed:\n' + '\n'.join(stage['diagnostics']))


def package_tests(runner, package):
    """Exercise native TEST blocks, extended tests, and an installed-only copy."""
    # Native check/install can generate documentation; use a disposable source copy.
    source = runner.scratch / 'source'
    shutil.copytree(package.parent, source)
    copied = source / package.name
    original = copied.read_text()
    default = 'Configuration => { "alpha" => "paper", "parameters" => "generic" }'
    if original.count(default) != 1:
        raise ValueError('package default configuration changed; review native test setup')
    for config in ('paper', 'paper2'):
        runner.begin_batch('package_' + config)
        # check starts fresh M2 processes without forwarding Configuration. Change
        # only the default in this disposable copy so its children test that mode.
        copied.write_text(original.replace(default, default.replace('"paper"', quote(config))))
        runner.run('native_' + config, setup(copied, config) +
                   'assert(#(tests ExceptionalDiagrams)==5);\n'
                   f'check ExceptionalDiagrams;\nprint {quote(DONE)};\nexit 0;\n')
        groups = [(g, None, None) for g in ('recipes', 'context', 'identities')]
        groups += [('restrictions', i, chunk) for i in range(5)
                   for chunk in (range(4) if config == 'paper2' and i == 1 else [None])]
        for group, index, chunk in groups:
            suffix = group + (f'_{index}' if index is not None else '')
            suffix += f'_range_{chunk}' if chunk is not None else ''
            runner.run('extended_' + config + '_' + suffix, command=[runner.m2, '--script',
                       str(source / 'tests/exceptional-diagrams.m2'), config, 'generic', 'basic',
                       group] + ([str(index)] if index is not None else [])
                       + ([str(chunk)] if chunk is not None else []))
    runner.begin_batch('installation')
    prefix = runner.scratch / 'installed'
    copied.write_text(original)
    runner.run('install', f'path=prepend({quote(str(source) + "/")},path);\n'
               f'installPackage("ExceptionalDiagrams", FileName=>{quote(copied)}, '
               f'InstallPrefix=>{quote(str(prefix) + "/")});\nprint {quote(DONE)};\nexit 0;\n')
    installed = prefix / 'share/Macaulay2/ExceptionalDiagrams.m2'
    if not installed.is_file():
        raise RuntimeError('installed package was not created under the requested prefix')
    # Remove the installation source before loading again in fresh processes.
    shutil.rmtree(source)
    for config in ('paper', 'paper2'):
        runner.run('installed_' + config, setup(installed, config) + f'''
assert(ExceptionalDiagrams#"source directory"=={quote(str(installed.parent) + '/')});
assert(b==cf and c==cf');
scan(11,i->(
    a:=rep(i,(braid(Dilute=>true))_1,Dilute=>true);
    b:=rep(i,(braid(Dilute=>true))_2,Dilute=>true);
    assert(a*b*a==b*a*b);
    r:=rep(i,(Rmatrix())_1,Dilute=>true);
    assert(numRows r==numRows a);
));
assert(#diagramList(3,3,Dilute=>true)==287);
assert(rep(0,idempotent(3,0),Dilute=>false)==id_(F^1));
print {quote(DONE)};
exit 0;
''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--m2', default='M2', help='Macaulay2 executable')
    parser.add_argument('--data-root', type=Path, default=ROOT / 'data')
    parser.add_argument('--representation', choices=NAMES, help='check just one representation')
    parser.add_argument('--package-tests', action='store_true', help='also test package and isolated installation')
    parser.add_argument('--output', type=Path, help='write a new JSON report; never overwrite one')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('output already exists')
    executable = shutil.which(args.m2)
    if not executable:
        parser.error('Macaulay2 executable not found: ' + args.m2)
    package = ROOT / 'macaulay2/ExceptionalDiagrams.m2'
    report = {'status': 'FAIL', 'field': 'QQ(p,q,u)', 'per_worker_seconds': 60,
              'batch_seconds': 300, 'package_tests_requested': args.package_tests}
    with tempfile.TemporaryDirectory(prefix='exceptional-m2-') as tmp:
        runner = Runner(executable, Path(tmp))
        try:
            report['macaulay2_version'] = subprocess.check_output(
                [executable, '--version'], text=True, timeout=10).strip()
            for index, name in enumerate(NAMES):
                if args.representation and name != args.representation:
                    continue
                for config in ('paper', 'paper2'):
                    program, labels, count = comparison_program(args.data_root.resolve(), package, index, config)
                    runner.run(name + '_' + config, program, labels=labels, matrices=count)
            if args.package_tests:
                package_tests(runner, package)
            report['status'] = 'PASS'
        except Exception as exc:
            report['error'] = str(exc)
            print(str(exc), file=sys.stderr)
        report['stages'] = runner.stages
        report['matrix_comparisons'] = sum(s['matrix_comparisons'] for s in runner.stages)
        report['seconds'] = round(time.monotonic() - runner.started, 3)
    report['input_sha256'] = {
        'macaulay2/' + str(p.relative_to(package.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(package.parent.rglob('*.m2'))}
    report['input_sha256'].update({
        'data/' + str(p.relative_to(args.data_root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(args.data_root.rglob('*.json'))})
    for name in ('tools/check_macaulay2_data.py', 'tools/validate_data.py'):
        report['input_sha256'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    print(f"{report['status']}: {report['matrix_comparisons']} matrix comparisons")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
