#!/usr/bin/env python3
"""Offline structural validation. No CAS, matrix identities, or code evaluation."""
import argparse, copy, hashlib, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
from jsonschema import Draft7Validator, RefResolver
from validate_data import (Invalid, require, loads, parse_scalar, identifiers,
                           scalar, coefficient_order, semantic_validate,
                           validate_algebra, validate_collection)
ROOT=Path(__file__).resolve().parents[1]

def read(path): return loads(path.read_text())
def reference(owner, name, required=True):
 path=(owner.parent/name).resolve()
 require(path.is_relative_to(ROOT),f'outside-repository runtime reference: {name}')
 if required:require(path.is_file(),f'missing reference: {name}')
 return path

def definitions(defs,variables):
 coefficient_order({'coefficients':defs,'field':{'variables':variables}})
 return set(defs)|set(variables)

def matrices(doc,names,operators):
 n=doc['dimension'];order=doc['basis']['order']
 require(len(order)==len(set(order))==n,'basis length/uniqueness mismatch')
 require([m['operator'] for m in doc['matrices']]==operators,'generator order/reference mismatch')
 for m in doc['matrices']:
  require(m['rows']==m['cols']==n,'matrix dimension mismatch')
  coords=[]
  for i,j,s in m['entries']:
   require(0<=i<n and 0<=j<n,'sparse index out of bounds')
   tree=scalar(s,names);require(tree!=('int',0),'literal stored zero')
   coords.append((i,j))
  require(coords==sorted(set(coords)),'duplicate or non-row-major sparse entries')
 if 'formula_ref' in doc:
  require([m['position'] for m in doc['matrices']]==[1,2],'spectral positions must be 1,2')

def words(terms,ops,names):
 for t in terms:
  scalar(t['coefficient'],names);require(set(t['word'])<=set(ops),'unknown generator word')

def validate(self_test=False):
 catalog=read(ROOT/'data/publication.json');entries=catalog['files'];paths=[e['path'] for e in entries]
 require(len(paths)==len(set(paths)),'duplicate catalog path')
 require(set(paths)=={str(p.relative_to(ROOT)) for p in (ROOT/'data').rglob('*.json')},'catalog does not cover exactly data/**/*.json')
 schemas={p.as_uri():read(p) for p in (ROOT/'schema').glob('*.json')}
 def blocked(uri):raise Invalid('nonlocal schema: '+uri)
 docs={}
 for item in entries:
  path=reference(ROOT/'catalog',item['path']);sp=reference(ROOT/'catalog',item['schema']);doc=read(path);sch=schemas[sp.as_uri()]
  Draft7Validator.check_schema(sch)
  resolver=RefResolver(sp.as_uri(),sch,store=schemas,handlers={'http':blocked,'https':blocked,'file':blocked})
  Draft7Validator(sch,resolver=resolver).validate(doc)
  if '$schema' in doc:require(reference(path,doc['$schema'])==sp,'catalog/schema mismatch')
  docs[item['path']]=doc
 local=docs['data/local_a2.json'];algebra=docs['data/a3.json'];semantic_validate(local);validate_algebra(algebra)
 ordinary_names=definitions({**local['coefficients'],**algebra['coefficients']},['p','q'])
 reps=[docs[f'data/representations/{r["id"]}.json'] for r in algebra['representations']];validate_collection(reps)
 for d in reps:matrices(d,ordinary_names,algebra['operator_order'])
 for registry,count in [('data/dilute_a3.json',30),('data/dilute_a2.json',16)]:
  reg=docs[registry];expected=[('G' if count==30 else 'D')+str(i) for i in range(count)]
  require(reg['operator_order']==[g['operator'] for g in reg['generators']]==expected,'registry generator order')
  defs={k:{'expression':reg['normalization_prescriptions'][k]} for k in ('alpha','beta')};names=definitions(defs,['p','q'])
  for g in reg['generators']:
   for key in ('paper_multiplier','paper2_multiplier'):scalar(g[key],names)
  for r in reg['representations']:
   path=reference(ROOT/registry,r['file']);d=docs[str(path.relative_to(ROOT))]
   require(d['id']==r['id'] and d['dimension']==r['dimension'],'registry representation mismatch')
   require(reference(path,d['algebra_ref'])==ROOT/registry,'algebra reference mismatch')
   matrices(d,{'p','q'},expected)
 formula=docs['data/spectral_r.json'];emb=docs['data/dilute_a3_embeddings.json']
 fnames=definitions(formula['coefficient_definitions'],['p','q','u'])
 require(reference(ROOT/'data/spectral_r.json',formula['generators_ref'])==ROOT/'data/dilute_a3_embeddings.json','formula generators ref')
 require(reference(ROOT/'data/dilute_a3_embeddings.json',emb['coefficient_import'])==ROOT/'data/local_a2.json','embedding coefficients ref')
 require(reference(ROOT/'data/dilute_a3_embeddings.json',emb['raw_generators_ref'])==ROOT/'data/dilute_a3.json','embedding raw generators ref')
 require(emb['local_diagram_ids']==['D'+str(i) for i in range(16)],'local diagram inventory')
 require(set(emb['positions'])=={'1','2'},'embedding positions')
 for pos,blocks in emb['positions'].items():require(set(blocks)=={str(i) for i in range(16) if i!=4},'incomplete local embeddings')
 for terms in emb['generator_expressions'].values():words(terms,emb['local_diagram_ids'],set(local['coefficients'])|{'p','q'})
 words(emb['local_D4_definition'],emb['local_diagram_ids'],{'p','q'})
 words(formula['generator_expansion'],emb['generator_expressions'],fnames)
 scalar(formula['scalar_relationship']['normalization_scalar'],fnames)
 crossing=formula['crossing'];require(set(crossing['spectral_substitution'])=={'p','q','u'},'crossing variables')
 for s in crossing['spectral_substitution'].values():scalar(s,{'p','q','u'})
 rotations=sum(crossing['rotation_pairs'],[])+crossing['fixed_generators']
 require(set(rotations)<=set(emb['generator_expressions']) and len(rotations)==len(set(rotations)),'rotation generator references')
 require([v['u'] for v in formula['distinguished_values']]==['0','1','infinity'],'distinguished value inventory')
 for v in formula['distinguished_values']:
  scalar(v['rescale'],fnames);scalar(v['coefficient'],fnames);require(v['generator'] in emb['generator_expressions'],'limit generator ref')
 for i in range(11):
  path=ROOT/f'data/spectral/Dilute_{i}.json';d=docs[str(path.relative_to(ROOT))];source=docs[f'data/dilute_representations/Dilute_{i}.json']
  require(d['id']==source['id'] and d['dimension']==source['dimension'] and d['basis']==source['basis'] and d['conventions']==source['conventions'],'spectral source coordinates mismatch')
  for key,target in [('representation_ref',f'data/dilute_representations/Dilute_{i}.json'),('formula_ref','data/spectral_r.json'),('embeddings_ref','data/dilute_a3_embeddings.json'),('algebra_ref','data/dilute_a3.json')]:require(reference(path,d[key])==ROOT/target,'spectral cross-reference mismatch')
  matrices(d,definitions(d['coefficient_definitions'],['p','q','u']),['Rpoly1','Rpoly2'])
 maps=docs['data/basis_maps.json'];mapnames=set(local['coefficients'])|{'alpha','beta','p','q'}
 for name in maps['coefficient_imports']:reference(ROOT/'data/basis_maps.json',name)
 require(len(maps['occupancy_decompositions'])==11,'occupancy collection incomplete')
 for rep in maps['occupancy_decompositions']:
  d=docs[str(reference(ROOT/'data/basis_maps.json',rep['representation_ref']).relative_to(ROOT))]
  require([b['coordinate'] for b in rep['basis']]==list(range(d['dimension'])),'occupancy coordinate order')
  for b in rep['basis']:
   require(b['occupancy']==sorted(set(b['occupancy'])) and set(b['occupancy'])<={0,1,2},'invalid occupancy')
   algebra_name,label=b['ordinary_space'].split(':')
   if algebra_name=='A3':
    source=docs[f'data/representations/{label}.json'];require(0<=b['ordinary_coordinate']<source['dimension'],'ordinary coordinate ref')
   else:require(algebra_name in ('A2','A1','A0') and b['ordinary_coordinate']==0,'local character coordinate')
 for m in maps['maps']:
  d=docs[str(reference(ROOT/'data/basis_maps.json',m['representation_ref']).relative_to(ROOT))]
  require(m['basis_order']==d['basis']['order'] and len(m['matrix_diagonal'])==d['dimension'],'basis map dimensions/order')
  for s in m['matrix_diagonal']:scalar(s,mapnames)
  reference(ROOT/'catalog',m['evidence'],required=False)
 for p in catalog['verification_evidence']:reference(ROOT/'catalog',p,required=False)
 prov=docs['data/publication_provenance.json']
 require(set(prov['payload_hashes'])==set(paths)-{'data/publication_provenance.json'}|{str(p.relative_to(ROOT)) for p in (ROOT/'schema').glob('*.json')},'provenance payload coverage')
 for p,h in prov['payload_hashes'].items():require(hashlib.sha256(reference(ROOT/'catalog',p).read_bytes()).hexdigest()==h,'payload hash mismatch: '+p)
 negatives=[]
 if self_test:
  template=docs['data/spectral/Dilute_0.json'];names=definitions(template['coefficient_definitions'],['p','q','u'])
  mutations=[('index_bounds',lambda d:d['matrices'][0]['entries'][0].__setitem__(0,d['dimension'])),('duplicate_coordinate',lambda d:d['matrices'][0]['entries'].append(d['matrices'][0]['entries'][0])),('unknown_scalar',lambda d:d['matrices'][0]['entries'][0].__setitem__(2,'undeclared')),('dimension',lambda d:d['matrices'][0].__setitem__('rows',1)),('position',lambda d:d['matrices'][0].__setitem__('position',2)),('basis',lambda d:d['basis']['order'].pop()),('generator',lambda d:d['matrices'][0].__setitem__('operator','unknown'))]
  for name,mutate in mutations:
   bad=copy.deepcopy(template);mutate(bad)
   try:matrices(bad,names,['Rpoly1','Rpoly2'])
   except Invalid:negatives.append(name)
   else:raise Invalid('negative accepted: '+name)
  for name,func in [('coefficient_cycle',lambda:definitions({'a':{'expression':'b'},'b':{'expression':'a'}},['p','q'])),('scalar_code',lambda:parse_scalar('__import__(1)')),('missing_ref',lambda:reference(ROOT/'data/test','missing.json'))]:
   try:func()
   except Invalid:negatives.append(name)
   else:raise Invalid('negative accepted: '+name)
 return {'status':'PASS','kind':'structural_only','json_files':len(paths),'schemas':len(schemas),'matrix_files':sum('matrices' in d for d in docs.values()),'matrices':sum(len(d.get('matrices',[])) for d in docs.values()),'negative_fixtures_rejected':negatives,'limitations':'Structural validation checks schemas, expressions, references and hashes. Exact identity checks are recorded separately.'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--output',type=Path);args=parser.parse_args();started=time.monotonic()
 try:result=validate(args.self_test)
 except Exception as exc:result={'status':'FAIL','error':str(exc)}
 result['seconds']=time.monotonic()-started;print(json.dumps(result,indent=2))
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 return 0 if result['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
