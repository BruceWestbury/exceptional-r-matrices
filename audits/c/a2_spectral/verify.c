#include "exact.h"
/* New A2 mathematics: diagram-linear construction and denominator-cleared
 * integer-polynomial matrix products. Not the C YBE construction algorithm. */
static J *spec,*formula,*embedding,*registry;
static int failed=0;
static const char *operators[]={"one","S_dilute","Sinv_dilute","K","T","B","E","U","O"};
static const char *splitnames[]={"I","U","S_ordinary","Sinv_ordinary","K","H","E","D_squared","T","D","O"};
static Rat *vector(int n){Rat *v=calloc(n,sizeof *v);for(int i=0;i<n;i++)init(v+i);return v;}
static void release(Rat *v,int n){for(int i=0;i<n;i++)clear(v+i);free(v);}
static void accumulate(Rat *r,const Rat *a,const Rat *b){Rat t;init(&t);op(&t,a,b,'*');op(r,r,&t,'+');clear(&t);}
static int idx(const char *s){for(int i=0;i<11;i++)if(!strcmp(s,splitnames[i]))return i;die("split generator");return 0;}
static void emit(const Rat *r){char *n=fmpz_mpoly_get_str_pretty(r->n,vars,ctx),*d=fmpz_mpoly_get_str_pretty(r->d,vars,ctx);printf("{\"numerator\":\"%s\",\"denominator\":\"%s\"}",n,d);flint_free(n);flint_free(d);}
static void residual(const Rat *r){emit(r);if(!fmpz_mpoly_is_zero(r->n,ctx))failed=1;}
static void environment(const char *substitution){
 for(int i=0;i<ne;i++){clear(&env[i].r);free(env[i].name);}ne=0;
 for(int i=0;i<3;i++){env[ne].name=strdup(vars[i]);init(&env[ne].r);fmpz_mpoly_gen(env[ne].r.n,i,ctx);ne++;}
 if(substitution){Rat z;init(&z);expr(&z,substitution);set(&env[2].r,&z);clear(&z);}
}
static void merge(J *a,J *b){for(int i=0;i<b->n;i++){a->a=realloc(a->a,(a->n+1)*sizeof(J*));a->a[a->n++]=b->a[i];}}
static void normal(Rat *r){expr(r,get(get(formula,"scalar_relationship"),"normalization_scalar")->s);}
static Rat *coefficients(int poly){
 Rat *c=vector(9);
 if(!poly){J *obj=get(spec,"rational_coefficients");for(int i=0;i<9;i++)expr(c+i,get(obj,operators[i])->s);}
 else {J *terms=get(formula,"generator_expansion");for(int t=0;t<terms->n;t++){J *term=terms->a[t],*w=get(term,"word");if(w->n!=1)die("coefficient word");int i;for(i=0;i<9;i++)if(!strcmp(w->a[0]->s,operators[i]))break;if(i==9)die("spectral generator");expr(c+i,get(term,"coefficient")->s);}}
 return c;
}
static void normalization_check(const char *substitution){
 environment(substitution);Rat *r=coefficients(0),*p=coefficients(1);Rat n,t;init(&n);init(&t);normal(&n);printf("{");
 for(int i=0;i<9;i++){op(&t,&n,r+i,'*');op(&t,p+i,&t,'-');printf("%s\"%s\":",i?",":"",operators[i]);residual(&t);}printf("}");release(r,9);release(p,9);clear(&n);clear(&t);
}
/* Expand the split diagram combinations into the published D0,...,D15 basis.
 * D3 D3 denotes the declared basis element D4, not a new matrix fitting. */
static void expand(Rat *out,const char *name,const Rat *c){
 J *terms=get(get(embedding,"generator_expressions"),name);Rat s;init(&s);
 for(int i=0;i<terms->n;i++){J *t=terms->a[i],*w=get(t,"word");int d;
  if(w->n==1)d=atoi(w->a[0]->s+1);
  else if(w->n==2&&!strcmp(w->a[0]->s,"D3")&&!strcmp(w->a[1]->s,"D3"))d=4;
  else die("nonlinear diagram word");
  if(d<0||d>=16)die("diagram index");
  expr(&s,get(t,"coefficient")->s);accumulate(out+d,c,&s);
 }clear(&s);
}
static Rat *splitcoeff(int poly){
 Rat *c=coefficients(poly),*s=vector(11);J *splits=get(spec,"splits");
 for(int i=0;i<9;i++){J *labels=get(splits,operators[i]);for(int j=0;j<labels->n;j++){int k=idx(labels->a[j]->s);op(s+k,s+k,c+i,'+');}}release(c,9);return s;
}
static Rat *diagramcoeff(int poly){Rat *s=splitcoeff(poly),*v=vector(16);for(int i=0;i<11;i++)expand(v,splitnames[i],s+i);release(s,11);return v;}
static void skein(Rat *s){
 J *rule=get(spec,"skein"),*rep=get(rule,"replacement");int k=idx(get(rule,"eliminate")->s);Rat c,t;init(&c);init(&t);set(&c,s+k);integer(s+k,0);
 for(int i=0;i<rep->n;i+=2){expr(&t,rep->a[i+1]->s);accumulate(s+idx(rep->a[i]->s),&c,&t);}clear(&c);clear(&t);
}
static void crossing(void){
 const char *sub=get(get(spec,"substitutions"),"crossing")->s;
 int rotation[11];for(int i=0;i<11;i++)rotation[i]=-1;
 J *rot=get(formula,"crossing"),*pairs=get(rot,"rotation_pairs"),*fixed=get(rot,"fixed_generators");
 for(int i=0;i<pairs->n;i++){J *p=pairs->a[i];int a=idx(p->a[0]->s),b=idx(p->a[1]->s);rotation[a]=b;rotation[b]=a;}
 for(int i=0;i<fixed->n;i++){int a=idx(fixed->a[i]->s);rotation[a]=a;}
 for(int i=0;i<11;i++)if(rotation[i]<0)die("incomplete rotation");
 printf("\"diagram_residuals\":{");
 for(int poly=0;poly<=1;poly++){
  environment(NULL);Rat *a=splitcoeff(poly),pref;init(&pref);if(poly)integer(&pref,1);else expr(&pref,get(spec,"crossing_prefactor")->s);
  environment(sub);Rat *b=splitcoeff(poly),*v=vector(11),*d=vector(16),t;init(&t);
  for(int i=0;i<11;i++)set(v+rotation[i],a+i);
  for(int i=0;i<11;i++){op(&t,&pref,b+i,'*');op(v+i,v+i,&t,'-');}
  environment(NULL);skein(v);for(int i=0;i<11;i++)expand(d,splitnames[i],v+i);
  printf("%s\"%s\":{",poly?",":"",poly?"polynomial":"rational");for(int i=0;i<16;i++){printf("%s\"D%d\":",i?",":"",i);residual(d+i);}printf("}");
  release(a,11);release(b,11);release(v,11);release(d,16);clear(&pref);clear(&t);
 }printf("},\"scalar_residuals\":{");
 Rat na,nb,pref,t,z;init(&na);init(&nb);init(&pref);init(&t);init(&z);
 environment(NULL);normal(&na);expr(&pref,get(spec,"crossing_prefactor")->s);
 expr(&t,get(get(get(formula,"crossing"),"spectral_substitution"),"u")->s);expr(&z,sub);op(&t,&t,&z,'-');printf("\"declared_substitution\":");residual(&t);
 environment(sub);normal(&nb);expr(&t,sub);environment(NULL);op(&t,&t,lookup("u"),'-');printf(",\"crossing_substitution_involution\":");residual(&t);
 op(&t,&na,&pref,'*');op(&z,&t,&nb,'-');printf(",\"N_times_prefactor_minus_transformed_N\":");residual(&z);
 printf(",\"normalization_u\":");normalization_check(NULL);printf(",\"normalization_crossed\":");normalization_check(sub);printf("},\"polynomial_crossing_factor\":");op(&t,&t,&nb,'/');emit(&t);printf(",");
 clear(&na);clear(&nb);clear(&pref);clear(&t);clear(&z);
}
static Rat *matrix(J *doc,const char *sub){
 environment(sub);int n=ji(get(doc,"dimension"));Rat *a=vector(n*n),*coef=diagramcoeff(1);J *ms=get(doc,"matrices"),*gs=get(registry,"generators");Rat mult,entry,c;init(&mult);init(&entry);init(&c);
 for(int k=0;k<16;k++){
  J *m=ms->a[k];if(strcmp(get(m,"operator")->s,get(gs->a[k],"operator")->s))die("generator ordering");
  expr(&mult,get(gs->a[k],"paper2_multiplier")->s);op(&c,coef+k,&mult,'*');J *entries=get(m,"entries");
  for(int j=0;j<entries->n;j++){J *e=entries->a[j];int r=ji(e->a[0]),col=ji(e->a[1]);if(r<0||col<0||r>=n||col>=n)die("matrix index");expr(&entry,e->a[2]->s);accumulate(a+r*n+col,&entry,&c);}
 }release(coef,16);clear(&mult);clear(&entry);clear(&c);return a;
}
static void common_denominator(fmpz_mpoly_t d,Rat *a,int n){
 fmpz_mpoly_one(d,ctx);fmpz_mpoly_t g;fmpz_mpoly_init(g,ctx);
 for(int i=0;i<n;i++){if(!fmpz_mpoly_gcd(g,d,a[i].d,ctx))die("denominator gcd");fmpz_mpoly_divexact(g,a[i].d,g,ctx);fmpz_mpoly_mul(d,d,g,ctx);}fmpz_mpoly_clear(g,ctx);
}
static void unitarity(const char *name){
 char path[256];snprintf(path,sizeof path,"data/dilute_a2_representations/%s.json",name);J *doc=readj(path);int n=ji(get(doc,"dimension"));const char *inv=get(get(spec,"substitutions"),"inverse")->s;
 Rat *a=matrix(doc,NULL),*b=matrix(doc,inv),np,nm,t;init(&np);init(&nm);init(&t);environment(NULL);normal(&np);environment(inv);normal(&nm);op(&np,&np,&nm,'*');
 fmpz_mpoly_t da,db,den,g,prod,tmp;fmpz_mpoly_init(da,ctx);fmpz_mpoly_init(db,ctx);fmpz_mpoly_init(den,ctx);fmpz_mpoly_init(g,ctx);fmpz_mpoly_init(prod,ctx);fmpz_mpoly_init(tmp,ctx);
 common_denominator(da,a,n*n);common_denominator(db,b,n*n);fmpz_mpoly_mul(den,da,db,ctx);
 for(int i=0;i<n*n;i++){fmpz_mpoly_divexact(g,da,a[i].d,ctx);fmpz_mpoly_mul(a[i].n,a[i].n,g,ctx);fmpz_mpoly_divexact(g,db,b[i].d,ctx);fmpz_mpoly_mul(b[i].n,b[i].n,g,ctx);}
 Rat *r=vector(n*n);
 for(int i=0;i<n;i++)for(int j=0;j<n;j++){
  fmpz_mpoly_zero(prod,ctx);for(int k=0;k<n;k++){fmpz_mpoly_mul(tmp,a[i*n+k].n,b[k*n+j].n,ctx);fmpz_mpoly_add(prod,prod,tmp,ctx);}
  fmpz_mpoly_set(t.n,prod,ctx);fmpz_mpoly_set(t.d,den,ctx);norm(&t);if(i==j)op(&t,&t,&np,'-');set(r+i*n+j,&t);
 }
 printf("\"dimension\":%d,\"polynomial_residual_matrix\":[",n);
 for(int i=0;i<n;i++){printf("%s[",i?",":"");for(int j=0;j<n;j++){if(j)printf(",");residual(r+i*n+j);}printf("]");}printf("],\"rational_residual_matrix\":[");
 for(int i=0;i<n;i++){printf("%s[",i?",":"");for(int j=0;j<n;j++){if(j)printf(",");op(&t,r+i*n+j,&np,'/');residual(&t);}printf("]");}printf("],\"normalization_product\":");emit(&np);
 printf(",\"clearing_factors\":{");fmpz_mpoly_set(t.n,da,ctx);fmpz_mpoly_one(t.d,ctx);printf("\"u\":");emit(&t);fmpz_mpoly_set(t.n,db,ctx);printf(",\"inverse\":");emit(&t);printf("},\"coefficient_normalization_residuals\":{\"u\":");normalization_check(NULL);printf(",\"inverse\":");normalization_check(inv);printf("},");
 release(a,n*n);release(b,n*n);release(r,n*n);clear(&np);clear(&nm);clear(&t);fmpz_mpoly_clear(da,ctx);fmpz_mpoly_clear(db,ctx);fmpz_mpoly_clear(den,ctx);fmpz_mpoly_clear(g,ctx);fmpz_mpoly_clear(prod,ctx);fmpz_mpoly_clear(tmp,ctx);
}
int main(int argc,char **argv){
 if(argc!=2)die("usage: verify I|L|X2|Y2|Y2_star|crossing (repository cwd)");
 double start=now();fmpz_mpoly_ctx_init(ctx,3,ORD_LEX);
 spec=readj("audits/a2_spectral_spec.json");formula=readj("data/spectral_r.json");embedding=readj("data/dilute_a3_embeddings.json");registry=readj("data/dilute_a2.json");defs=get(readj("data/local_a2.json"),"coefficients");merge(defs,get(formula,"coefficient_definitions"));merge(defs,get(spec,"coefficient_definitions"));environment(NULL);bind("beta",get(get(registry,"normalization_prescriptions"),"beta")->s);
 /* beta is required after each environment reset: install a JSON definition. */
 const char *raw=get(get(registry,"normalization_prescriptions"),"beta")->s;char buffer[2048];snprintf(buffer,sizeof buffer,"{\"beta\":{\"expression\":\"%s\"}}",raw);const char *bp=buffer;merge(defs,json(&bp));
 printf("{\"task\":\"%s\",",argv[1]);if(!strcmp(argv[1],"crossing"))crossing();else unitarity(argv[1]);
 printf("\"calculation_seconds\":%.9f,\"flint\":\"%s\",\"status\":\"%s\"}\n",now()-start,flint_version,failed?"FAIL":"PASS");return failed?1:0;
}
