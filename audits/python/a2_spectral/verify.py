#!/usr/bin/env python3
"""Exact A2 audit: direct rational matrix products and formal diagram vectors.
No import of any prior audit or C implementation.
"""
import ast
import json
import sys
import time
from pathlib import Path
import flint
from flint import fmpq_mpoly_ctx
ROOT = Path(__file__).resolve().parents[3]
CTX = fmpq_mpoly_ctx.get(('p','q','u'), 'lex')

class Q:
    """Simple reduced quotient; monic denominators over Q[p,q,u]."""
    def __init__(self,n=0,d=1):
        n=CTX.constant(n) if isinstance(n,int) else n
        d=CTX.constant(d) if isinstance(d,int) else d
        if not d: raise ZeroDivisionError('zero denominator')
        g=n.gcd(d); n=n/g; d=d/g
        lead=d.leading_coefficient()
        self.n,self.d=n/lead,d/lead
    def __add__(self,b): return Q(self.n*b.d+b.n*self.d,self.d*b.d)
    def __neg__(self): return Q(-self.n,self.d)
    def __sub__(self,b): return self+-b
    def __mul__(self,b): return Q(self.n*b.n,self.d*b.d)
    def __truediv__(self,b): return Q(self.n*b.d,self.d*b.n)
    def __pow__(self,k): return Q(self.n**k,self.d**k) if k>=0 else Q(self.d**(-k),self.n**(-k))
    def __bool__(self): return bool(self.n)
    def output(self):return {'numerator':str(self.n),'denominator':str(self.d)}

P,UQ,U=(Q(x) for x in CTX.gens())
def read(p):return json.loads((ROOT/p).read_text())
SPEC=read('audits/a2_spectral_spec.json')
FORM=read('data/spectral_r.json')
EMB=read('data/dilute_a3_embeddings.json')
REG=read('data/dilute_a2.json')
DEFS={**read('data/local_a2.json')['coefficients'],**FORM['coefficient_definitions'],**SPEC['coefficient_definitions'],**{k:{'expression':REG['normalization_prescriptions'][k]} for k in ('alpha','beta')}}
class Scalars:
    def __init__(self,u):self.cache={'p':P,'q':UQ,'u':u};self.active=set()
    def name(self,k):
        if k not in self.cache:
            if k in self.active:raise ValueError('cyclic scalar '+k)
            self.active.add(k);self.cache[k]=self(DEFS[k]['expression']);self.active.remove(k)
        return self.cache[k]
    def __call__(self,s):
        def walk(t):
            if isinstance(t,ast.Constant) and type(t.value) is int:return Q(t.value)
            if isinstance(t,ast.Name):return self.name(t.id)
            if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.USub):return -walk(t.operand)
            if isinstance(t,ast.BinOp):
                if isinstance(t.op,ast.Pow):
                    e=t.right;sign=1
                    if isinstance(e,ast.UnaryOp) and isinstance(e.op,ast.USub):sign=-1;e=e.operand
                    if not isinstance(e,ast.Constant) or type(e.value) is not int:raise ValueError('integer exponent required')
                    return walk(t.left)**(sign*e.value)
                a,b=walk(t.left),walk(t.right)
                if isinstance(t.op,ast.Add):return a+b
                if isinstance(t.op,ast.Sub):return a-b
                if isinstance(t.op,ast.Mult):return a*b
                if isinstance(t.op,ast.Div):return a/b
            raise ValueError('invalid scalar syntax')
        return walk(ast.parse(s.replace('^','**'),mode='eval').body)

def zero(n):return [[Q() for _ in range(n)] for _ in range(n)]
def eye(n):return [[Q(int(i==j)) for j in range(n)] for i in range(n)]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def mul(a,b):
    n=len(a);out=zero(n)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if a[i][k] and b[k][j]:out[i][j]=out[i][j]+a[i][k]*b[k][j]
    return out

def coeffs(sc,poly=False):
    if not poly:return {k:sc(v) for k,v in SPEC['rational_coefficients'].items()}
    return {t['word'][0]:sc(t['coefficient']) for t in FORM['generator_expansion']}

def normalization(sc):return sc(FORM['scalar_relationship']['normalization_scalar'])
def coefficient_checks(sc):
    r,p=coeffs(sc),coeffs(sc,True);n=normalization(sc)
    return {k:(p[k]-n*r[k]).output() for k in r}
def allzero(res):
    if isinstance(res,dict):
        if 'numerator' in res:return res['numerator']=='0'
        return all(allzero(v) for v in res.values())
    return all(allzero(v) for v in res)

def unitarity(name):
    a=Scalars(U);b=Scalars(a(SPEC['substitutions']['inverse']))
    doc=read(f'data/dilute_a2_representations/{name}.json');n=doc['dimension'];ops={}
    for g,m in zip(REG['generators'],doc['matrices']):
        assert g['operator']==m['operator']
        x=zero(n)
        for i,j,s in m['entries']:x[i][j]=a(s)*a(g['paper2_multiplier'])
        ops[m['operator']]=x
    composite={}
    for op,terms in EMB['generator_expressions'].items():
        mat=zero(n)
        for t in terms:
            word=eye(n)
            for g in t['word']:word=mul(word,ops[g])
            mat=add(mat,scale(word,a(t['coefficient'])))
        composite[op]=mat
    def build(sc):
        mat=zero(n)
        for k,c in coeffs(sc).items():mat=add(mat,scale(composite[k],c))
        return mat
    residual=add(mul(build(a),build(b)),scale(eye(n),Q(-1)))
    rational=[[x.output() for x in row] for row in residual]
    poly=[[x.output() for x in row] for row in scale(residual,normalization(a)*normalization(b))]
    relation={'u':coefficient_checks(a),'inverse':coefficient_checks(b)}
    return {'task':name,'dimension':n,'status':'PASS' if allzero([rational,poly,relation]) else 'FAIL','rational_residual_matrix':rational,'polynomial_residual_matrix':poly,'normalization_product':(normalization(a)*normalization(b)).output(),'coefficient_normalization_residuals':relation,'method':'direct rational matrix product; polynomial residual obtained by exact N(u)N(u^-1) equivalence'}

def split(c):
    out={}
    for k,value in c.items():
        for g in SPEC['splits'][k]:out[g]=out.get(g,Q())+value
    return out

def reduce_diagrams(vector,sc):
    # Eliminate S by the explicit skein relation before diagram expansion.
    v=dict(vector);co=v.pop(SPEC['skein']['eliminate'],Q())
    for k,c in SPEC['skein']['replacement'].items():v[k]=v.get(k,Q())+co*sc(c)
    out={k:Q() for k in SPEC['diagram_basis']}
    for k,c in v.items():
        for term in EMB['generator_expressions'][k]:
            word=term['word'];g='D4' if word==['D3','D3'] else word[0]
            if len(word)!=1 and word!=['D3','D3']:raise ValueError('not a linear diagram term')
            out[g]=out[g]+c*sc(term['coefficient'])
    return out

def crossing():
    a=Scalars(U);b=Scalars(a(SPEC['substitutions']['crossing']))
    perm={k:k for k in FORM['crossing']['fixed_generators']}
    for x,y in FORM['crossing']['rotation_pairs']:perm[x]=y;perm[y]=x
    pref=a(SPEC['crossing_prefactor']);na,nb=normalization(a),normalization(b)
    residuals={}
    for poly in (False,True):
        left=split(coeffs(a,poly));right=split(coeffs(b,poly));rot={perm[k]:v for k,v in left.items()}
        factor=Q(1) if poly else pref
        v={k:rot.get(k,Q())-factor*right.get(k,Q()) for k in perm}
        residuals['polynomial' if poly else 'rational']={k:v.output() for k,v in reduce_diagrams(v,a).items()}
    checks={'N_times_prefactor_minus_transformed_N':(na*pref-nb).output(),'crossing_substitution_involution':(b(SPEC['substitutions']['crossing'])-U).output(),'declared_substitution':(a(FORM['crossing']['spectral_substitution']['u'])-a(SPEC['substitutions']['crossing'])).output(),'normalization_u':coefficient_checks(a),'normalization_crossed':coefficient_checks(b)}
    return {'task':'crossing','status':'PASS' if allzero([residuals,checks]) else 'FAIL','diagram_residuals':residuals,'scalar_residuals':checks,'polynomial_crossing_factor':(na*pref/nb).output(),'method':'formal rotation, skein elimination, expansion into sixteen diagram coordinates; no representation evaluation'}

if __name__=='__main__':
    start=time.monotonic();task=sys.argv[1]
    result=crossing() if task=='crossing' else unitarity(task)
    result.update(calculation_seconds=time.monotonic()-start,python=sys.version.split()[0],python_flint=flint.__version__,flint=flint.__FLINT_VERSION__)
    print(json.dumps(result,indent=2));sys.exit(0 if result['status']=='PASS' else 1)
