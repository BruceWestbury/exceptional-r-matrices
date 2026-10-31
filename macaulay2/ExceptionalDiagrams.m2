newPackage("ExceptionalDiagrams",
    Version => "0.2",
    Date => "2026 October 6",
    Authors => {{Name => "Paul Zinn-Justin",
            Email => "pzinn@unimelb.edu.au",
            HomePage => "http://blogs.unimelb.edu.au/paul-zinn-justin/"}},
    Headline => "Diagrams for the exceptional series",
    DebuggingMode => true,
    AuxiliaryFiles => true,
    Configuration => { "alpha" => "paper", "parameters" => "generic" }
)

-* TODO
* disp
* convert all booleans to Dilute options (matrix...)
* put back decompose/matrix stuff, removed because of failure of @ product, see diagrams.m2
*-

α = (options ExceptionalDiagrams).Configuration#"alpha";
parameters = (options ExceptionalDiagrams).Configuration#"parameters";

export {
    "diagramList", "diagram", "diagramId", "Diagram", "Diagram1",
    "Dilute", "Strands",
    "move", "reflect", "inner", "closure",
    "δ", "ϕ", "τ", "ξ", "ζ", "ζ'",
    "skein",
    "braid", "Rmatrix",
    "bar", "bracket",
    "cutLength", "selectCutLength",
    "p" => "p", "q" => "q", "u" => "u", "v" => "v", -- dirty trick to avoid error, though could use it to do something fun (font?)
    "F" => "F",
    "b" => "b", "c" => "c",
    "idempotent", "rep"
    }
exportMutable {
     "skeinLevel"
     }


prefix := ExceptionalDiagrams#"source directory"|"ExceptionalDiagrams/" -- or could use currentFileDirectory
myget = s -> value get (prefix|s)


debug Core -- for precedence concatCols frame and a few more

Diagram1 = new Type of BasicList -- a single diagram
-- syntax: {#out,#in,list of edges}
Diagram = new Type of VirtualTally -- a linear combination of them
RingElement * Diagram := lookup(symbol *,Number,VirtualTally) -- to fix recent breaking change of cd27cf14e03e1e5b1ee4c1becac79611529bb9e0

partial := d -> (l:=flatten d#2; any(d#0+d#1,i->not member(i,l))) -- try to guess Dilute or not
Diagram_ZZ := (d,n) -> (
    dilute := any(keys d,partial);
    if n==1 then d**diagramId(1,Dilute=>dilute) else diagramId(n-1,Dilute=>dilute)**d -- because I keep using E_1, E_2 etc. but what about dilute/not?
    )
Diagram1_ZZ := (d,n) -> (diagram d)_n

try needsPackage "Factor" else ( factor Ring := opts -> identity; factored := identity );
if parameters === "generic" then (
    --    p=getSymbol "p"; q=getSymbol "q"; u=getSymbol "u";v= getSymbol "v";
    F0=QQ;
    R=factor(ZZ[p,q,u,v,DegreeRank=>0]);F=frac R;
    p=F_0; q=F_1; u=F_2; v=F_3;
    r=1/q^2; t=p^2; z=u^2; w=v^2; -- TODO stop using those
    ) else if parameters === "random" then (
    F0=ZZ/32749;
    R=factor(F0[u,v,DegreeRank=>0]);F=frac R;
    p=random F0; q=random F0;
    r=1/q^2; t=p^2; z=u^2; w=v^2; -- TODO stop using those
    ) else if parameters === "allrandom" then (
    F0=R=F=ZZ/32749;
    p=random F0; q=random F0; u=random F0; v=random F0;
    r=1/q^2; t=p^2; z=u^2; w=v^2; -- TODO stop using those    
    ) else if class parameters === Sequence and #parameters!=0 then (
    F0=frac ring first parameters;
    R=factor(F0[u,v,DegreeRank=>0]);F=frac R;
    p=parameters#0; q=parameters#1; -- TODO allow more flexibility in how many params are specialised
    r=1/q^2; t=p^2; z=u^2; w=v^2; -- TODO stop using those
    ) else error "invalid value of \"parameters\""

-- use sf font for variables
debug Core
sf = new Type of Expression
texMath sf := a -> "\\mathsf{"|texMath a#0|"}"
toExternalFormat sf := net sf := toString sf := a -> toString a#0
expressionValue sf := a -> expressionValue a#0
(monoid R).generatorExpressions=apply((monoid R).generatorExpressions,a->new sf from {a})
--

δ=-(((1 + t^2)*(-1 + r*t^5)*(r - t^6))/((-1 + r)*(r - t)*t^6));
ϕ=(t^3+r)*(1+r*t^2)*(1-t)^2*(1+t+t^2)^3/(t^6*(t-r)*(1-r));

-- to make it easier to renormalise
renorm = method()
--renorm Diagram := d -> sum(pairs d,(k,v)->v*renorm k)
renorm Diagram := d -> sum(pairs d,(k,v)->v*scale k*k) -- more optimised
renorm Diagram1 := d -> scale d*d  

scale1 = α -> d -> α^(-( -- this is rescaling of cup/cup which will break the left/right symmetry
    v:=unique flatten d#2; -- vertices including bdry occupied ones
    sum(v,i->if i>=d#0 then 1 else -1) -- (|D|+n-m)/2 where |D| is the number of vertices, m/n is the number of left/right bdry legs
    )//2)
scale2 = β -> d -> β^(-( -- alternatively one can rescale the trivalent vertex, but that changes α by a square
    v:=unique flatten d#2; -- vertices including bdry occupied ones
    number(v,i->i>=d#0+d#1)
))

if α==="paper2" then ( -- differs from the above by a [n+1]
    β:=(q-1)*(q+1)*p^3/(q*(p-1)*(p+1)*(p^2-p+1)*(p^2+p+1));
    α=β^2;
    scale=scale2 β;
    ) else (
    if α==="paper" then -- turn into paper conventions
    α=1/(q^2*p^(-1)*(p-1)^2*(p+1)^2*(p-1+p^(-1))^2*(p+1+p^(-1))^2/((q-1)*(q+1)*(q*p-1)*(q*p+1)));
    scale = scale1 α;
    )
ϕ=ϕ*α;
τ= ϕ*t*(t+1)*(r*t^4+r^2*t^2-r*t^3+r^2*t-r*t^2+t^3-r*t+t^2+r)/((t^2+t+1)*(t^3+r)*(r*t^2+1)); -- any ϕ

cf=myget "cf.m2";
cf'=myget "cfprime.m2";
-- Export named coefficient values so installPackage can document their symbols.
b=cf;
c=cf';

-*
ξ=(q-1)*(q+1)*(p*q-1)*(p*q+1)/(q^2*p);
ζ=-(q-1)*(q+1)*(p^4+q^2)/(q^2*p*(p-1)*(p+1));
ζ'=(p*q-1)*(p*q+1)*(p^6*q^2+1)/(q^2*p^3*(p-1)*(p+1));
*-
ξ=α*(p-1)^2*(p+1)^2*(p^2-p+1)^2*(p^2+p+1)^2/p^6;
ζ=α*-(p-1)*(p+1)*(p^2-p+1)^2*(p^2+p+1)^2*(p^4+q^2)/(p^6*(q*p-1)*(q*p+1));
ζ'=α*(p-1)*(p+1)*(p^2-p+1)^2*(p^2+p+1)^2*(q^2*p^6+1)/(p^8*(q-1)*(q+1));


needsPackage "VectorGraphics"

zeroDiagram = new Diagram from {}
-- this is also generic for virtual tallies viewed as formal linear combinations
expression Diagram := d -> Sum apply(pairs d,(k,v) -> v*expression k)
net Diagram := net @@ expression
texMath Diagram := texMath @@ expression
toString Diagram := toString @@ expression

dst:=new MutableHashTable;
dist=(i,l) -> ( -- distance function to vertex i in edge list l
    scan(flatten l,j->dst#j=infinity);
    dst#i=0; n:=0; flag:=true;
    while flag do (
        flag=false;
        scan(l, a -> (
	    	if dst#(a#0)==n and dst#(a#1)==infinity then ( dst#(a#1)=n+1; flag=true; )
	    	else if dst#(a#1)==n and dst#(a#0)==infinity then ( dst#(a#0)=n+1; flag=true; )
                ));
        n=n+1;
        );
    new HashTable from dst
    )

cmpfun0 := cmpfun := (x,y) -> x?y -- temporary def
Cmp = new Type of Holder
Cmp ? Cmp := (x,y) -> cmpfun(x#0,y#0)

h:=new MutableHashTable;
-- careful that unique uses it too
oldunique = keys @@ set
mysort = d -> ( -- print("in",d#2);
    n:=d#0+d#1;
    l:=d#2;
    v:=oldunique select(flatten l,i->i>=n);
    cp := new MutableList;
    cmpfun = if n>0 then (x,y) -> (
        i:=0;
        while (if i==#cp then cp#i=dist(i,l);
            i<n-1 and cp#i#x===cp#i#y) do i=i+1;
        cp#i#x ? cp#i#y
        ) else cmpfun0; -- sadly, havent found anything better        
    v=apply(sort apply(v,i->new Cmp from {i}),c->c#0);
    scan(#v,i->h#(v#i)=i+n);
    l=sort(sort\applyTable(l,i->if i<n then i else h#i)); -- print("out",l);
    new Diagram1 from {d#0,d#1,l}
    )

diagram = method()
diagram (ZZ,ZZ,List) := (a,b,l) -> diagram mysort new Diagram1 from {a,b,l}
diagram Diagram1 := d -> new Diagram from { d => 1_F }
diagram Diagram := identity

diagram1 = method()
diagram1 Diagram := d -> if #d!=1 then error "applies to single diagram only" else first keys d
diagram1 Diagram1 := identity
diagram1 (ZZ,ZZ,List) := (a,b,l) -> mysort new Diagram1 from {a,b,l}
Diagram _ Diagram := (d,d') -> d_(diagram1 d')

skeinLevel = 5 -- default level = everything except trimming

-- probably useless: shouldn't directly manipulate Diagram1 (why not? rethink carefully)
Number*Diagram1 := RingElement*Diagram1 := (r,d) -> if r==0 then zeroDiagram else new Diagram from {d=>r};
Diagram+Diagram1:=(d,d')->d+diagram d'
Diagram1+Diagram:=(d,d')->diagram d+d'
Diagram1+Diagram1:=(d,d')->diagram d+diagram d'
Diagram-Diagram1:=(d,d')->d-diagram d'
Diagram1-Diagram:=(d,d')->diagram d-d'
Diagram1-Diagram1:=(d,d')->diagram d-diagram d'
Diagram1*Diagram1:=(d,d')->skein(d|d')
Diagram1*Diagram:=(d,d')->(diagram d)*d'
Diagram*Diagram1:=(d,d')->d*(diagram d')
Diagram1|Diagram:=(d,d')->(diagram d)|d'
Diagram|Diagram1:=(d,d')->d|(diagram d')
Diagram==Diagram1:=(d,d')->d==diagram d'
Diagram1==Diagram:=(d,d')->diagram d==d'
Diagram1==Diagram1:=(d,d')->d===d'
Diagram1^ZZ:=(d,n)->(diagram d)^n
Diagram1**Diagram:=(d,d')->(diagram d)**d'
Diagram**Diagram1:=(d,d')->d**(diagram d')
Diagram1||Diagram:=(d,d')->(diagram d)||d'
Diagram||Diagram1:=(d,d')->d||(diagram d')

pastefun=
Diagram1|Diagram1 := (d,d') -> ( -- product with no skeinning
    if d#1 =!= d'#0 then error "diagrams can't be combined";
    mx := max(max flatten d#2+1-(d#0+d#1),0);
    relabel1 := i -> if i<d#0 then i else i+d'#1;
    relabel2 := i -> if i<d'#0 then d'#0-1-i+d#0+d'#1 else if i<d'#0+d'#1 then i-d'#0+d#0 else i+d#0+mx;
    l := applyTable(d#2,relabel1)|applyTable(d'#2,relabel2);
    mysort new Diagram1 from {d#0,d'#1,l} -- better to sort already
    )
Diagram|Diagram := (d,d') -> combine(d,d',pastefun,times,plus)
Diagram*Diagram := (d,d') -> skein(d|d')

insertfun=
insert(List,Diagram1,Diagram1) := (l,d1,d) -> ( -- insert d1 inside d where external vertices are l
    if #l != d1#0+d1#1 then error "wrong arguments";
    mx := max(max flatten d#2+1,d#0+d#1);
    mysort new Diagram1 from {d#0,d#1,d#2 | applyTable(d1#2,i->if i<#l then l#i else i-#l+mx)}
    )
insert(List,Diagram,Diagram1) := (l,d1,d) -> insert(l,diagram1 d1,d)

chain = memoize((k,l) -> ( -- find a k-chain based on a list of edges (multiple edges not considered, can't go thru same vertex twice)
    if k<1 then return {};
    if k==1 then return oldunique flatten l;
    if k==2 then return l | apply(l,reverse);
    c1:=chain(k-1,l); c2:=chain(2,l);
    flatten apply(c1,c->
        apply(select(c2,e->c#(-1)==e#0 and not isMember(e#1,c)),e->append(c,e#1))
        )
    ))
-- the following shouldn't really be memoized -- or only internally in skein
ichain = memoize((k,l) -> ( -- same, except c#0 == min c, used by loop to kill cyclic rotations
    if k<1 then return {};
    if k==1 then return oldunique flatten l;
    if k==2 then return l;
    c1:=ichain(k-1,l); c2:=chain(2,l);
    flatten apply(c1,c->
        apply(select(c2,e->c#(-1)==e#0 and c#0<e#1 and not isMember(e#1,c)),e->append(c,e#1))
        )
    ))
loop = memoize((k,l) -> ( -- find a k-loop in a list of edges
    if k<1 then return {};
    if k==1 then return apply(select(l,a->a#0==a#1),first);
    if k==2 then return keys(select(tally l, v->v==2));
    select(ichain(k,l),c->isMember({c#0,c#-1},l) and c#1<c#-1) -- last condition to kill reflection symmetry
    ))


-- in skein, it's assumed that i<j in each edge {i,j}
skein = method()
skein Diagram := d -> if #d==0 then d else sum(pairs d,(k,v)->v*skein k)
skein Diagram1 := d -> skein(d#0,d#1,d#2,skeinLevel) -- just convenient
skein (Diagram,ZZ) := (d,level) -> if #d==0 then d else sum(pairs d,(k,v)->v*skein(k,level))
skein (Diagram1,ZZ) := (d,level) -> skein(d#0,d#1,d#2,level)

skein(ZZ,ZZ,List,ZZ) := memoize( (n1,n2,l,level) -> (
    -- valency 2 vertices can be removed
    -- can't have dangling lines in the middle
    -- can't have tadpoles
    -- closed loops have a weight of δ
    -- print l;
    mx := max flatten l;
    i:=n1+n2;
    while i<=mx do (
        ll:=select(l,a -> a#0==i or a#1==i);
        if #ll == 1 and ll#0 == {i,i} then (
            -- closed loop
            return δ*skein(n1,n2,delete({i,i},l),level);
            )
        else if #ll == 1 then return zeroDiagram -- dangling
        else if any(ll, a -> a == {i,i}) then return zeroDiagram -- tadpoles
        else if #ll == 2 then (
            -- valency 2
	    -- return skein(n1,n2,append(delete(ll#1,delete(ll#0,l)),sort delete(i,ll#0|ll#1))); -- recursing is a waste
	    l=append(delete(ll#1,delete(ll#0,l)),sort delete(i,ll#0|ll#1));
	    i=n1+n2;
            )
        else if level>1 and #ll == 3 and #(lll:=oldunique ll)<3 then ( -- multiple edge
            -- for trivalent graphs, only 2 cases to consider
            if #lll==1 then (
                return δ*ϕ*skein(n1,n2,delete(lll#0,l),level);
                ) else (
                return ϕ*skein(n1,n2,append(delete(lll#1,delete(lll#0,l)),sort delete(i,lll#0|lll#1)),level);
                )
            )
	else i=i+1;
        );
    -- more advanced (should be done *after* basic ones)
    -- triangles
    --    print("investigating", diagram(n1,n2,l));
    --    s:=subsets(toList(n1+n2..mx),3);
    --    p:=position(s,a->all(subsets(a,2),b->isMember(b,l)));
    if level<3 then return diagram(n1,n2,l);
    s:=loop(3,l);
    if #s>0 then (
        -- found a triangle
        i=s#0#0; i1:=s#0#1; i2:=s#0#2;
        return τ*skein(n1,n2,sort\delete({i,i},applyTable(l,j->if j==i1 or j==i2 then i else j)),level);
        );
    -- double squares (should be done *after* triangles)
    if level<4 then return diagram(n1,n2,l);
    ss:=apply(loop(4,l),set);-- squares
    for a in ss do for a' in ss do if #(a*a')==2 then -- pairs of squares with 2 vertices in common
    if class cf === Symbol then print "warning: square/square" else (
	-- found such a pair: replace it with linear combination of first 4 (2,2) tangles
	b:=a+a'; -- the 6 vertices
	b0:=toList(a*a'); -- the middle 2
	b1:=toList(a-a'); b2:=toList(a'-a); -- the 4 external ones
	if not isMember(sort {b0#0,b1#0},l) then b1=reverse b1; -- reorder
	if not isMember(sort {b0#0,b2#0},l) then b2=reverse b2; -- reorder
	l=select(l,c->not isSubset(c,b)); -- remove all edges connecting them
	return skein(sum(#cf,i->cf_i*insert({b1#0,b1#1,b2#1,b2#0},fulllst2_i,new Diagram1 from {n1,n2,l})),level);
        -- sum(skein insert) might seem more natural but there's a small chance of simplification -- could we be even more clever?
	);
    -- square pentagon
    if level<5 then return diagram(n1,n2,l);
    ss':=apply(loop(5,l),set);-- pentagons
    for a in ss do for a' in ss' do if #(a*a')==2 then -- square/pentagon pair with 2 vertices in common
    if class cf' === Symbol then print "warning: square/pentagon" else (
        b:=a+a'; -- the 7 vertices
	b0:=toList(a*a'); -- the middle 2
	b1:=toList(a-a'); b2:=toList(a'-a); -- the 5 external ones
	if not isMember(sort {b0#0,b1#0},l) then b1=reverse b1; -- reorder
        b2a:=position(b2,i->isMember(sort{b0#0,i},l)); b2c:=position(b2,i->isMember(sort{b0#1,i},l)); b2b:=3-(b2a+b2c);
        b2=b2_{b2a,b2b,b2c}; -- reorder
	l=select(l,c->not isSubset(c,b)); -- remove all edges connecting them
        return skein(sum(#cf',i->cf'_i*insert({b1#0,b1#1,b2#2,b2#1,b2#0},fulllst23_i,new Diagram1 from {n1,n2,l})),level);
        );
    -- square hexagon? currently disabled since doesn't do anything anyway
    -*
    s'':=subsets(toList(n1+n2..mx),6);
    ss'':=select(s'',a->number(subsets(a,2),b->isMember(b,l))==6);-- hexagons
    sss'':=ss**ss'';
    p=position(sss'',a->#(set a#0*set a#1)==2); -- square/hexagon pair with 2 vertices in common
    if p=!=null then (
        print "warning: square/hexagon";
--        return zeroDiagram; -- TEMP
        );
    *-
    -- ran out of skein rels => just keep as is (up to mysorting)
    if level<6 then diagram(n1,n2,l) else trim diagram1(n1,n2,l)
    ))

Diagram^ZZ := (d,n) -> if n==1 then d else if n>1 then d*(d^(n-1)) else if n==0 and #d>0 and (d1:=first keys d; d1#0==d1#1) then id_(d1#0) else error "not implemented" -- TODO n=0

tensorfun=
Diagram1||Diagram1 :=
Diagram1**Diagram1 := (d,d') -> (
    mx := max(max flatten d#2+1-(d#0+d#1),0);
    relabel1 := i -> if i<d#0 then i else i+d'#0+d'#1;
    relabel2 := i -> if i<d'#0+d'#1 then i+d#0 else i+d#0+d#1+mx;
    l := applyTable(d#2,relabel1)|applyTable(d'#2,relabel2);
    mysort new Diagram1 from {d#0+d'#0,d#1+d'#1,l}
    )
Diagram||Diagram :=
Diagram**Diagram := (d,d') -> combine(d,d',tensorfun,times,plus)

Diagram^**ZZ := (d,n) -> if n==0 then closedDiagram else if n==1 then d else if n>1 then d**(d^**(n-1)) else error "not implemented"

-- moving external vertices from one side to the other
move = method()
move (ZZ,ZZ,Diagram) := (n1,n2,d) -> applyKeys(d,dd -> move(n1,n2,dd))
move (ZZ,ZZ,Diagram1) := (n1,n2,d) -> if n1+n2!=d#0+d#1 then error "wrong number of external vertices" else new Diagram1 from {n1,n2,d#2}

-- rotating external vertices
rotate (ZZ,Diagram) := (k,d) -> applyKeys(d,dd -> rotate(k,dd))
rotate (ZZ,Diagram1) := (k,d) -> mysort new Diagram1 from {d#0,d#1,
    applyTable(d#2,i->if i>=d#0+d#1 then i else (i+k)%(d#0+d#1))}

-- reflect external vertices
reflect = method()
reflect Diagram := d -> applyKeys(d,reflect)
reflect Diagram1 := d -> mysort new Diagram1 from {d#1,d#0,
    applyTable(d#2,i->if i>=d#0+d#1 then i else d#0+d#1-1-i)}

closedDiagram=new Diagram1 from {0,0,{}}
inner = method()
inner (Diagram1,Diagram1) := (d,d') -> inner(diagram d,diagram d')
inner (Diagram1,Diagram) := (d,d') -> inner(diagram d,d')
inner (Diagram,Diagram1) := (d,d') -> inner(d,diagram d')
inner (Diagram,Diagram) := (d,d') -> (
    if d===zeroDiagram or d'===zeroDiagram then return 0;
    d1:=first keys d;
    n:=d1#0+d1#1;
    d=move(0,n,d);
    d'=move(n,0,d');
    d'':=d*d';
    m:=#d'';
    if m==0 then 0 else if m==1 and first keys d'' === closedDiagram then first values d'' else error "failed to compute"
    )

diagramId = method(Options => {Dilute => false}, TypicalValue => Diagram)
diagramId ZZ := o -> i -> if o.Dilute then sum(subsets i, s -> diagram(i,i,apply(s,j->{j,2*i-1-j}))) else diagram(i,i,apply(i,j->{j,2*i-1-j}))

closure = method()
closure Diagram1 := d -> closure diagram d
closure Diagram := d -> (
    if d===zeroDiagram then return 0;
    d1:=first keys d;
    if d1#0!=d1#1 then error "can't close diagram" else inner(d,diagramId (d1#0))
)

hh:=new MutableHashTable;
split = d -> if d#0==0 or d#1==0 then true else ( -- if a Diagram1 is not connected between 2 sides
    scan(flatten d#2,i->hh#i=false); -- potential bug if vertex not present? TODO clarify
    scan(d#0,i->hh#i=true);
    flag:=true;
    while flag do (
        flag=false;
        for i from 0 to #(d#2)-1 do (
            if hh#(d#2#i#0) and not hh#(d#2#i#1) then if d#2#i#1<d#0+d#1 then return false else flag=hh#(d#2#i#1)=true
            else if hh#(d#2#i#1) and not hh#(d#2#i#0) then if d#2#i#0<d#0+d#1 then return false else flag=hh#(d#2#i#0)=true;
            ));
    return true;
)

cutLength = method()
cutLength Diagram := d -> max apply(keys d,cutLength)
-- cutLength Diagram := cutLength @@ diagram1
cutLength Diagram1 := memoize ( d -> (
    n:=#(d#2);
    for i from 0 to n do (
        s := subsets(d#2,n-i);
        for j from 0 to #s-1 do
        if split(d#0,d#1,s#j) then return i;
        )
    ))

selectCutLength = (c,d) -> applyPairs(d,a->if cutLength a#0==c then a)

-- some bases
empty = (m,n) -> diagram(m,n,{})

empty1 = diagram1(1,1,{})
full1 = diagram1 diagramId 1
lst1={full1,empty1};

tri12 = diagram1 (1,2,{{0,3},{1,3},{2,3}})

empty2 = diagram1 ( 2, 2, {} )
leftid2  = diagram1 ( 2, 2, {{0,3}} )
rightid2 = diagram1 ( 2, 2, {{1,2}} )
full2 = diagram1 diagramId 2
cap = diagram1 ( 2, 2, {{0,1}} )
cup = diagram1 ( 2, 2, {{2,3}} )
U = diagram1 ( 2, 2, {{0,1},{2,3}} )
K = diagram1 ( 2, 2, {{0,4},{1,4},{2,5},{3,5},{4,5}})
H = diagram1 ( 2, 2, {{0,4},{1,5},{3,4},{2,5},{4,5}})
diagidb = diagram1( 2, 2, {{0,2}} )
diagida = diagram1( 2, 2, {{1,3}} )
Yaa = diagram1( 2, 2, {{1,4},{2,4},{3,4}} )
Yba = diagram1( 2, 2, {{0,4},{2,4},{3,4}} )
Yab = diagram1( 2, 2, {{0,4},{1,4},{3,4}} )
Ybb = diagram1( 2, 2, {{0,4},{1,4},{2,4}} )
fulllst2={full2,U,K,H,diagram1(H*H)}
lst2=fulllst2|{leftid2,diagida,diagidb,rightid2,Yaa,Yba,Yab,Ybb,cup,cap,empty2}

-- a few more useful ones
H1 = H||full1; H2=full1||H;
K1 = K||full1; K2=full1||K;
U1 = U||full1; U2=full1||U;


-- would be basis of full (2,3)
-- 4 basic kinds
disc23  = diagram1 (2,3,{{0,1},{2,5},{3,5},{4,5}}) -- disconnected
tree23  = diagram1 (2,3,{{0,5},{1,6},{2,6},{3,7},{4,5},{5,7},{6,7}}) -- tree
sq23    = diagram1 (2,3,{{0,5},{1,5},{2,6},{3,7},{4,8},{5,9},{9,6},{6,7},{7,8},{8,9}}) -- square
penta23 = diagram1 (2,3,{{0,5},{1,6},{2,7},{3,8},{4,9},{5,6},{6,7},{7,8},{8,9},{9,5}}) -- pentagon
fulllst23=apply(5,i->rotate(i,disc23))|apply(5,i->rotate(i,tree23))|apply(5,i->rotate(i,sq23))|{penta23};
addHole = (k,d,b) -> new Diagram1 from {d#0+if b then 1 else 0,d#1+if b then 0 else 1,applyTable(d#2,i->if i<k then i else i+1)}
lst23= fulllst23 | unique flatten table(5,lst2,(k,x)->addHole(k,x,false))


fulllst33=myget "basis33.m2";
lst33 = fulllst33 | unique flatten table(6,lst23,(k,x)->addHole(k,x,true));
-- standard sort
sfun = d -> (d#0,d#1,#(d#2),-#(set flatten d#2),d#2)
Diagram1 ? Diagram1 := (d,d') -> sfun d ? sfun d'

sortByCuts = l -> reverse apply(sort apply(#l,i->(cutLength l#i,i)), a -> l#(a#1)) -- is sorting by cuts such a good idea?

diagramList0 := memoize ( (m,n,partial) -> (
	if m+n>6 then error "not implemented";
	sortByCuts apply(diagramList0((m+n)//2,(m+n+1)//2,partial),x->move(m,n,x))),
    {
	(0,0,false) => {diagram closedDiagram},
	(0,0,true) => {diagram closedDiagram},
	(0,1,false) => {},
	(0,1,true) => {empty(0,1)},
	(1,1,false) => {diagram full1},
	(1,1,true) => diagram\lst1,
	(1,2,false) => {diagram tri12},
	(1,2,true) => {tri12,diagram(1,2,{{0,1}}),diagram(1,2,{{0,2}}),diagram(1,2,{{1,2}}),empty(1,2)},
	(2,2,false) =>  (diagram\fulllst2),
	(2,2,true) =>  (diagram\lst2),
	(2,3,false) =>  (diagram\fulllst23),
	(2,3,true) => (diagram\lst23),
	(3,3,false) => diagram \ fulllst33,
	(3,3,true) => (diagram\ lst33)
	}
    )
diagramList = method(Options => {Dilute => false})
diagramList (ZZ,ZZ) := o -> (m,n) -> diagramList0(m,n,o.Dilute)

-- converting diagrams to vectors
vector(Diagram,List) := (d,l) ->     vector apply(l,x->d_(diagram1 x))
vector Diagram := d -> (
    if d === zeroDiagram then return 0; -- problematic
    d1:=first keys d;
    m:=d1#0; n:=d1#1;
    vector (d,diagramList(m,n,Dilute=>any(keys d,partial)))
    )

-- inverse conversion
diagram(Vector,List) := (v,l) -> new Diagram from apply(l,entries v,(d,a)->if a!=0 then diagram1 d=>a) -- sum(#l, i -> v_i * l#i)
diagram (Vector,ZZ,ZZ) := (v,m,n) -> diagram(v,diagramList(m,n))

-*
concat = l -> ( -- a version of concatCols for vectors including possible 0s
    if #l==0 then return 0;
    -- determine common target
    V := oldunique nonnull apply(l, x -> if x=!=0 then class promote(x,F));
    if #V == 0 then return 0;
    if #V != 1 then error "cannot concatenate";
    V=V#0;
    l = apply(l, x -> if x === 0 then map(V,F^1,0) else matrix x);
    concatCols l
    )
*-
concat = l -> ( -- a version of concatCols for vectors including possible 0s
    if #l==0 then return 0;
    -- determine common target
    V := oldunique nonnull apply(l, x -> if x=!=0 then class promote(x,F));
    if #V == 0 then return 0;
    if #V != 1 then error "cannot concatenate";
    V=V#0;
    l = apply(l, x -> if x === 0 then toList(rank V:0) else entries x);
    matrix transpose l
    )

-- trimming = attempting to expand on given basis
trimD = null -- only load if needed 
trim Diagram1 := opts -> d -> (
    if trimD === null then (try factored (R,true); trimD = myget "trim.m2"; try factored(R,false));
    if trimD#?d then (scale d)^-1 * renorm trimD#d else diagram d
    )
trim Diagram := opts -> d -> (
    if #d==0 then return d;
    if debugLevel>0 then (
        d1:=first keys d;
        n1:=d1#0; n2:=d1#1;
        l:=diagram1\diagramList(n1,n2,true);
        l':=set keys d - set l;
        print("intruders",keys l',toExternalString\keys l')
        );
    if d#0#0+d#0#1!=6 then return d;
    -- TODO treat d#0+d#1==6, d#0!=3
    sum(pairs d, (k,v) -> v*trim k) 
    )

-*
-- converting diagrams to (left multiplication) matrices
matrix(Diagram,List) :=
matrix(Diagram,Boolean) := o -> (d,a) -> sum(pairs d,(k,v)->v*matrix(k,a))
matrix Diagram := o -> d -> matrix(d,any(keys d,partial))
mat1 := memoize((d,partial) -> (
    if decTable#?d and #(decTable#d)>1 then
    product(decTable#d,d'->matrix(gensvalues#d',partial)) else (
        concat apply(diagramList(d#1,d#1,partial),d'->vector(skein(d|d',6),partial)) -- TODO suboptimal, see @
        )
    ))
matrix (Diagram1,Boolean) := o -> mat1 -- annoying interaction options/memoize
matrix Diagram1 := o -> d -> matrix(d,partial d)
mat2 := memoize((d,l) -> (
    if decTable#?d and #(decTable#d)>1 then
        product(decTable#d,d'->matrix(gensvalues#d',l)) else (
            concat apply(l,d'->vector(skein(d|d',6),l)) -- TODO suboptimal, see @ -- note 2 lists could be different
            )
        ))
matrix (Diagram1,List) := o -> mat2 -- annoying interaction options/memoize
*-
    

-- visualizing diagrams
-- TODO deal with diagrams with no external edges -- lack of planarity might be an issue
precedence Diagram1 := x -> precedence symbol symbol
expression Diagram1 := hold

eps=.1 -- "amount of nonlinearity" -- the lower, the higher
tsf=method()
tsf(Matrix,Number):=(M,m) -> matrix transpose apply(rank source M,i->entries tsf(M_i,m))
tsf(Vector,Number):=(V,m) -> ( -- nonlinear transform unit disk -> rectangle [-1,1] x [-eps,m+eps]
    y:=0.5*(1+V_1)*(m+2*eps)-eps;
    vector{V_0/sqrt(1-V_1^2),y}
    )
tsfi=method()
tsfi(Matrix,Number):=(M,m) -> matrix transpose apply(rank source M,i->entries tsfi(M_i,m))
tsfi(Vector,Number):=(V,m) -> ( -- nonlinear transform rectangle -> unit disk
    y:=(V_1+eps)/(m+2*eps)*2-1;
    vector{V_0*sqrt(1-y^2),y}
    )

vglabels=false -- switch to true to see numbering of vertices
vground=false
vgSize=20
vg = d -> if vground then roundvg d else normalvg d -- TODO unify the 2 functions into 1
pathwidth=.0266;
bgcolor="rgb(204,204,255)";
pathcolor="red";
bgborder="blue";
blobs=true;
doubleedgecf=1;

adjustcf=0.01
adjustlevel=1
adjust = (r,n,sz,level) -> (
    if level == 0 then return r;
    diffs:=apply(sz,i->apply(i,j->(
                x:={r_(0,i)-r_(0,j),r_(1,i)-r_(1,j)};
                1/(x#0^2+x#1^2)*x
                )));
    adjust(matrix table(2,sz,(k,i)->(
            r_(k,i)+if i<n then 0 else adjustcf*sum(sz,j->if j<i then diffs#i#j#k else if j>i then -diffs#j#i#k else 0)
            )),n,sz,level-1)
    );

normalvg = d -> (
    n1 := d#0;
    n2 := d#1;
    l := d#2;
    mx := max(n1,n2)-1;
    n := n1+n2;
    ll:=oldunique flatten l;
    sz := max(n,1+max ll);
    if n==0 then return LITERAL (if #l==0 then "$\\varnothing$" else "?");-- gList(); -- TEMP what if it's a nontrivial closed diagram? -- in principle, if all skein relations are there, shouldn't happen
    m := mutableMatrix(RR,sz,sz);
    scan(l, a -> if a#0 != a#1 then ( -- TODO treat loops?
            m_(a#0,a#1)=m_(a#0,a#1)+1;
            m_(a#1,a#0)=m_(a#1,a#0)+1;
            m_(a#0,a#0)=m_(a#0,a#0)-1;
            m_(a#1,a#1)=m_(a#1,a#1)-1;
            ));
    r := tsfi(matrix{{n1:-1., n2:1.},{apply(reverse(0..n1-1),y->y+max(0,n2-n1)*.5),apply(0..n2-1,y->y+max(0,n1-n2)*.5)}},mx);
    if sz>n then ( -- to avoid bugs with RR mutable matrices
        m1 := m^{n..sz-1}_{n..sz-1};
        m2 := m^{n..sz-1}_{0..n-1};
        m3 := - matrix solve(m1,m2);
        rr := r*transpose m3;
        r=r | rr;
        );
    -- split points on top of each other
    r=mutableMatrix r; eps1:=.5/(mx+1);
    scan(n..<sz,i -> scan(i, j -> (
                if 10*abs(r_(0,i)-r_(0,j))+abs(r_(1,i)-r_(1,j))<2*eps1 then (--print("before",i,j,r_(1,i),r_(1,j));
                    avg:=.5*(r_(1,i)+r_(1,j));
                    if r_(1,i)>r_(1,j) then ( r_(1,i)=avg+eps1; r_(1,j)=avg-eps1; ) else ( r_(1,i)=avg-eps1; r_(1,j)=avg+eps1; );
                    --print("after",i,j,r_(1,i),r_(1,j));
                    )
                )));
    --    r=matrix r;
    r=adjust(r,n,sz,adjustlevel);
    --
    tsf1 := if n1==0 then (v->vector{2*v_0-1,v_1})@@tsf else if n2==0 then (v->vector{2*v_0+1,v_1})@@tsf else tsf;
    t:=tally l; -- in case of multiple edges
    border:=.4;
    pathwidth1:=pathwidth*sqrt((4+(mx+2*border)^2)/8);
    spots:=partition(i->isMember(i,ll),0..sz-1);
    gList(
        gList(
            Polygon{{[-1,-border],[-1,mx+border],[1,mx+border],[1,-border]},"tikz"=>"clip"},
            Polygon{{[-1,-border],[-1,mx+border],[1,mx+border],[1,-border]},"stroke"=>"none","fill"=>bgcolor},
            gList flatten (
                apply(pairs t, (a,k) -> (
                        r1:=tsf1(r_(a#0),mx); r2:=tsf1(r_(a#1),mx);
			midr:=tsf1(.5*(r_(a#0)+r_(a#1)),mx); if abs(r1_0+r2_0)>1.99 then midr+=vector{if r1_0<0 then .5 else -.5,0};
                        --                Line{tsf(r_(a#0),mx),tsf(r_(a#1),mx)}
			if k==1 then Path{{"M",r1,"Q",midr,r2}} --  Path{{"M",r1,"Q",(midr:=tsf1(.5*(r_(a#0)+r_(a#1)),mx)),r2}}
                        else Path{{"M",r1,"Q", midr+doubleedgecf*vector {r1_1-r2_1,r2_0-r1_0},r2,"Q",midr-doubleedgecf*vector {r1_1-r2_1,r2_0-r1_0},r1}} -- TODO: k>2
                        )),
                "stroke-width"=>pathwidth1,
                "stroke"=>pathcolor
                ),
            Polygon{{[-1,-border],[-1,mx+border],[1,mx+border],[1,-border]},"stroke"=>bgborder,"stroke-width"=>.25*pathwidth1}
            ),
        if vglabels then gList (apply(0..sz-1,i->GraphicsText{tsf1(r_i,mx),toString i,FontSize=>.1*sqrt n})|("text-anchor"=>"middle","dominant-baseline"=>"middle","stroke"=>"none","fill"=>"gray"))
	else if blobs then
        (if spots#?true then gList (apply(spots#true,i->Circle {tsf1(r_i,mx),pathwidth1*sqrt(mx+1)}) |("stroke-width"=>.05*pathwidth1,"stroke"=>"black", "fill" => pathcolor)),
        if spots#?false then gList (apply(spots#false,i->Circle {tsf1(r_i,mx),pathwidth1*sqrt(mx+1)}) | ("stroke-width"=>.05*pathwidth1,"stroke"=>"black", "fill" => "white")))
--        else if spots#?false then gList (apply(spots#false,i->gNode(tsf1(r_i,mx),Polygon {{[-.1,-.1],[-.1,.1],[.1,.1],[.1,-.1]}})) | ("stroke-width"=>.05*pathwidth1,"stroke"=>"black", "fill" => "white")),
        else if spots#?false then gList apply(spots#false,i->GraphicsHtml{tsf1(r_i,mx),"","tikz"=>"rectangle,inner sep=2pt",FontSize=>5.6*pathwidth1,"stroke-width"=>.05*pathwidth1,"stroke"=>"black", "fill" => "white"}), -- bit of a hack, only works with tikz
        Size=>vgSize
        )
)

--nrm = v -> sqrt(v_0^2+v_1^2)
nrm = v -> (v_0^2+v_1^2)

roundvg = d -> ( -- a variation where endpoints are regularly spaced around a circle
    n := d#0+d#1;
    n1 := d#0; -- only used for overall rotation
    l := d#2;
    ll:=oldunique flatten l;
    sz := max(n,1+max ll);
    if n==0 then return LITERAL (if #l==0 then "$\\varnothing$" else "?");-- gList(); -- TEMP what if it's a nontrivial closed diagram? -- in principle, if all skein relations are there, shouldn't happen
    m := mutableMatrix(RR,sz,sz);
    scan(l, a -> if a#0 != a#1 then ( -- TODO treat loops?
            m_(a#0,a#1)=m_(a#0,a#1)+1;
            m_(a#1,a#0)=m_(a#1,a#0)+1;
            m_(a#0,a#0)=m_(a#0,a#0)-1;
            m_(a#1,a#1)=m_(a#1,a#1)-1;
            ));
    r := matrix{apply(n,i->-cos(2*pi*(i-(n1-1)/2)/n)),apply(n,i->-sin(2*pi*(i-(n1-1)/2)/n))};
    if sz>n then ( -- to avoid bugs with RR mutable matrices
        m1 := m^{n..sz-1}_{n..sz-1};
        m2 := m^{n..sz-1}_{0..n-1};
        m3 := - matrix solve(m1,m2);
        rr := r*transpose m3;
        r=r | rr;
        );
    -- TODO split points otherwise adjust will mess up
    --    r=matrix r;
    r=adjust(r,n,sz,adjustlevel);
    t:=tally l; -- in case of multiple edges
    g:=gList (
        Circle{[0,0],1,"tikz"=>"clip"},
        Circle{[0,0],1,"fill"=>bgcolor,"stroke"=>"none"},
        gList flatten (
            --        Circle{[0,0],1,"stroke"=>bgborder,"fill"=>bgcolor,"stroke-width"=>.3*pathwidth},
            apply(pairs t, (a,k) -> (
                    r1:=r_(a#0); r2:=r_(a#1);
                    --                Line{tsf(r_(a#0),mx),tsf(r_(a#1),mx)}
                    if k==1 then -- Line{r1,r2}
                    --Path{{"M",r1,"C",if a#0<n then 0.7*r1+0.1*r2 else r1,if a#1<n then 0.7*r2+0.1*r1 else r2,r2}}
                    Path{{"M",r1,"C",if a#0<n then 1/(1+.6*nrm(r1-r2))*r1 else r1,if a#1<n then 1/(1+.6*nrm(r1-r2))*r2 else r2,r2}}
                    else Path{{"M",r1,"Q", [.5*(r1_0+r2_0)+doubleedgecf*(r1_1-r2_1),.5*(r1_1+r2_1)+doubleedgecf*(r2_0-r1_0)] ,r2,"Q",[.5*(r1_0+r2_0)+doubleedgecf*(-r1_1+r2_1),.5*(r1_1+r2_1)+doubleedgecf*(-r2_0+r1_0)],r1}} -- TODO: k>2
                    )),
            "stroke-width"=>pathwidth,
            "stroke"=>pathcolor
            ),
        Circle{[0,0],1,"stroke"=>bgborder,"stroke-width"=>.25*pathwidth}
        );
    if vglabels then g=gList (g,gList (toSequence apply(sz,i->GraphicsText{r_i,toString i,FontSize=>.1*sqrt n})|{"text-anchor"=>"middle","dominant-baseline"=>"middle","stroke"=>"none","fill"=>"gray"}))
    else if blobs then g=gList(g,gList (toSequence apply(sz,i->Circle nonnull {r_i,pathwidth*2,if not isMember(i,ll) then "fill" => "white"}) | {"stroke-width"=>.05*pathwidth,"stroke"=>"black", "fill" => "gray"}));
    g ++ {Size=>vgSize}
)

html Diagram1 := html @@ vg
texMath Diagram1 := tex Diagram1 := tex @@ vg

-- coeffs of the 5 idempotents in full (2,2) -- order is I, L, X_2, Y_2, Y_2^*
idem2cf:=myget "idem2.m2";
idempotent=method()
idempotent(ZZ,ZZ) := memoize((k,i) -> (
	if k==2 then sum(5,j->idem2cf#i#j*lst2#j)
	else if k==3 then first(try factored(R,true); renorm myget ("idem3_"|toString i|".m2"),try factored(R,false))
	-- order is I, L, X_2, Y_2, Y_2^*, X_3, Y_3, Y_3^*, A, C, C^*
	else error "incorrect value of 1st argument"
	))

cfR0:={(r - r^2 - t + r*t + r^2*t + t^2 -    r*t^2 + r*t^4)/(r*(1 + t)*   (1 - t + t^2)^2),  -((t*(-r + r*t^2 - r^2*t^2 - t^3 -      r*t^3 + r^2*t^3 + t^4 - r*t^4))/   (r*(1 + t)*(1 - t + t^2)^2)),  ((-1 + t)*(1 + t + t^2)*(1 + r*t^2)*   (r + t^3)*(-r + 2*r*t - r^2*t -     t^2 + r^2*t^2 + t^3 - 3*r*t^3 +     r^2*t^3 + t^4))/(ϕ*(-1 + r)*r*   (r - t)*t^3*(1 + t)*(1 - t + t^2)^    2), ((-1 + t)*(1 + t + t^2)*   (1 + r*t^2)*(r + t^3)*   (-r^2 - t + 3*r*t - r^2*t - t^2 +     r^2*t^2 + t^3 - 2*r*t^3 + r*t^4))/  (ϕ*(-1 + r)*r*(r - t)*t^3*(1 + t)*   (1 - t + t^2)^2),  -(((-1 + t)^2*(1 + t + t^2)^2*    (1 + r*t^2)^2*(r + t^3)^2)/   (ϕ^2*(-1 + r)*r*(r - t)*t^5*(1 + t)*    (1 - t + t^2)^2))};
braid0:=-sum(5,i->cfR0#i * lst2#i) -- careful this is the restriction to 5x5 (others arent very interesting anyway at z=0)
braid = method(Options => {Dilute => false}, TypicalValue => Diagram)
installMethod(braid, o -> () -> if o.Dilute then braid0+lst2#6+lst2#7+lst2#15 else braid0)

-- the full R-matrix
substitute (Diagram,Option) := substitute (Diagram,List) := (X,s) -> select(applyValues(X,val->if instance(val,Number) then val else sub(val,s)),val->val!=0)
Diagram Sequence := (d,val) -> if #val === 0 or #d === 0 then d else if #val === 1 then sub(d,u=>val#0) else if #val === 2 then sub(sub(d,u=>val#0),v=>val#1) else error "wrong substitution"
Diagram Number := Diagram RingElement := (d,r) -> d (1:r)
Rmatrix0 := renorm myget "Rmat.m2"; -- renorm is supposed to take care of normalisation of ϕ (hack...)
Rmatrix = val -> Rmatrix0 val

bar = method()
barSubstitutions := () -> (
    if parameters =!= "generic" then error "bar requires generic parameters; apply bar before specialising";
    {p=>1/p,q=>1/q,u=>1/u,v=>1/v}
    )
bar Diagram := x -> sub(x,barSubstitutions())
bar Matrix := bar RingElement := x -> sub(x,barSubstitutions())
bar Number := identity

bracket = s -> (
    if not instance(s,List) then s=toList sequence s;
    fac:=F_s;
    (fac-1/fac)/(q-1/q)
    )

-- decompose
decTable=new HashTable from {
    false => new HashTable from {
	new Diagram1 from {3,3,{{0,6},{1,9},{2,12},{3,17},{4,14},{5,11},{6,7},{6,8},{7,9},{7,10},{8,10},{8,11},{9,12},{10,13},{11,14},{12,15},{13,15},{13,16},{14,16},{15,17},{16,17}}} => {5,2,2,5,5,2}, new Diagram1 from {3,3,{{0,1},{2,3},{4,5}}} => {0}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{8,10},{9,10},{9,11}}} => {2,5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{8,10},{9,11},{10,11}}} => {2,4,2}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,9},{4,11},{5,10},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {1,3,1,5}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,10},{4,11},{5,9},{6,7},{7,8},{7,9},{8,10},{9,11},{10,11}}} => {1,4,2}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11}}} => {5,2,2}, new Diagram1 from {3,3,{{0,6},{1,11},{2,14},{3,15},{4,13},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11},{9,12},{10,13},{11,14},{12,14},{12,15},{13,15}}} => {5,5,2,2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,12},{3,15},{4,14},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,10},{9,12},{10,13},{11,14},{12,15},{13,14},{13,15}}} => {2,5,2,5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,13},{5,12},{6,7},{6,8},{7,9},{8,9},{8,10},{10,11},{10,12},{11,13},{12,13}}} => {2,2,3,1,5}, new Diagram1 from {3,3,{{0,6},{1,10},{2,10},{3,11},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{8,11},{9,11}}} => {4,2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,11},{5,8},{6,7},{6,8},{7,9},{8,10},{9,10},{10,11}}} => {5,1,4}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,10},{4,7},{5,6},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {5,5,2}, new Diagram1 from {3,3,{{0,6},{1,6},{2,9},{3,9},{4,8},{5,7},{6,7},{7,8},{8,9}}} => {1,5}, new Diagram1 from {3,3,{{0,6},{1,9},{2,12},{3,15},{4,14},{5,8},{6,7},{6,8},{7,9},{7,10},{8,11},{9,12},{10,12},{10,13},{11,13},{11,14},{13,15},{14,15}}} => {5,2,4,2,5}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,15},{4,14},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11},{10,12},{11,13},{12,13},{12,14},{13,15},{14,15}}} => {5,2,2,5,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,12},{3,15},{4,14},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,12},{9,13},{10,13},{10,14},{11,14},{12,15},{13,15}}} => {2,5,5,2,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,12},{4,13},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,12},{10,12},{10,13},{11,13}}} => {2,4,2,2}, new Diagram1 from {3,3,{{0,1},{2,6},{3,7},{4,7},{5,6},{6,7}}} => {0,4}, new Diagram1 from {3,3,{{0,5},{1,4},{2,3}}} => {}, new Diagram1 from {3,3,{{0,6},{1,7},{2,10},{3,11},{4,11},{5,8},{6,7},{6,8},{7,9},{8,9},{9,10},{10,11}}} => {2,2,4}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,10},{5,6},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {2,5,5}, new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,11},{4,11},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{10,11}}} => {4,1,4}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,9},{4,11},{5,10},{6,7},{6,8},{8,9},{8,10},{9,11},{10,11}}} => {2,3,1,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,9},{4,8},{5,8},{6,7},{6,8},{7,9}}} => {5,1}, new Diagram1 from {3,3,{{0,6},{1,8},{2,9},{3,9},{4,7},{5,6},{6,7},{7,8},{8,9}}} => {5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,13},{4,12},{5,8},{6,7},{6,8},{7,9},{8,10},{9,10},{9,11},{10,12},{11,13},{12,13}}} => {2,5,2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,13},{4,12},{5,8},{6,7},{6,8},{7,9},{8,10},{9,11},{10,11},{10,12},{11,13},{12,13}}} => {2,4,2,5}, new Diagram1 from {3,3,{{0,5},{1,2},{3,4}}} => {3}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,10},{4,11},{5,11},{6,7},{6,8},{7,9},{8,9},{8,10},{10,11}}} => {2,2,3,1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,8},{4,9},{5,9},{6,7},{6,8},{8,9}}} => {2,3,1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,13},{4,12},{5,8},{6,7},{6,8},{7,9},{8,9},{9,10},{10,11},{10,12},{11,13},{12,13}}} => {2,2,5,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,3},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {2,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,8},{4,5},{6,7},{6,8},{7,9},{8,9}}} => {2,4,0}, new Diagram1 from {3,3,{{0,6},{1,9},{2,13},{3,17},{4,16},{5,12},{6,7},{6,8},{7,9},{7,10},{8,11},{8,12},{9,13},{10,11},{10,14},{11,15},{12,16},{13,14},{14,17},{15,16},{15,17}}} => {5,2,5,2,5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,12},{3,17},{4,16},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,12},{9,13},{10,13},{10,14},{11,14},{12,15},{13,15},{14,16},{15,17},{16,17}}} => {2,5,5,2,2,5}, new Diagram1 from {3,3,{{0,5},{1,6},{2,6},{3,7},{4,7},{6,7}}} => {4}, new Diagram1 from {3,3,{{0,3},{1,2},{4,5}}} => {3,0}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,10},{4,11},{5,11},{6,7},{7,8},{7,9},{8,10},{9,10},{9,11}}} => {1,4,1}, new Diagram1 from {3,3,{{0,6},{1,6},{2,9},{3,11},{4,10},{5,7},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {1,5,5}, new Diagram1 from {3,3,{{0,5},{1,6},{2,7},{3,9},{4,8},{6,7},{6,8},{7,9},{8,9}}} => {5,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,14},{4,15},{5,13},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11},{10,12},{10,13},{11,14},{12,14},{12,15},{13,15}}} => {2,2,4,2,2}, new Diagram1 from {3,3,{{0,6},{1,9},{2,12},{3,13},{4,11},{5,8},{6,7},{6,8},{7,9},{7,10},{8,11},{9,12},{10,11},{10,13},{12,13}}} => {5,2,5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,4},{5,6},{6,7}}} => {2,3}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,11},{4,10},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11}}} => {2,5,1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,8},{3,9},{4,9},{5,6},{6,7},{7,8},{8,9}}} => {2,4}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,4},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {2,2,3}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,13},{4,10},{5,8},{6,7},{6,8},{7,9},{8,10},{9,11},{9,12},{10,12},{11,13},{12,13}}} => {2,5,5,2}, new Diagram1 from {3,3,{{0,6},{1,11},{2,14},{3,17},{4,16},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11},{9,12},{10,13},{11,14},{12,14},{12,15},{13,15},{13,16},{15,17},{16,17}}} => {5,5,2,2,5,5}, new Diagram1 from {3,3,{{0,6},{1,2},{3,6},{4,7},{5,7},{6,7}}} => {3,1}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,7},{4,5},{6,7}}} => {5,0}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{8,9},{9,10},{10,11}}} => {2,2,5}, new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,8},{4,7},{5,6},{6,7},{7,8},{8,9}}} => {4,2}, new Diagram1 from {3,3,{{0,6},{1,2},{3,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {3,1,5}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,8},{4,9},{5,9},{6,7},{7,8},{8,9}}} => {1,3,1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,15},{4,14},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11},{10,12},{11,13},{12,13},{12,14},{13,15},{14,15}}} => {2,2,4,2,5}, new Diagram1 from {3,3,{{0,6},{1,6},{2,10},{3,10},{4,11},{5,9},{6,7},{7,8},{7,9},{8,10},{8,11},{9,11}}} => {1,5,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,10},{4,11},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,10}}} => {2,4,1}, new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,10},{4,11},{5,8},{6,7},{6,8},{7,9},{7,10},{8,11},{10,11}}} => {4,1,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,11},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10},{10,11}}} => {2,2,3,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,9},{4,9},{5,8},{6,7},{6,8},{8,9}}} => {2,3,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,3},{4,7},{5,6},{6,7}}} => {2}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,4},{5,7},{6,7}}} => {1,3}, new Diagram1 from {3,3,{{0,6},{1,8},{2,10},{3,11},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,11},{10,11}}} => {5,2,5}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,10},{4,8},{5,8},{6,7},{6,8},{7,9},{7,10},{9,11},{10,11}}} => {5,5,1}, new Diagram1 from {3,3,{{0,6},{1,9},{2,13},{3,14},{4,15},{5,12},{6,7},{6,8},{7,9},{7,10},{8,11},{8,12},{9,13},{10,13},{10,14},{11,14},{11,15},{12,15}}} => {5,2,4,2,2}, new Diagram1 from {3,3,{{0,6},{1,9},{2,12},{3,15},{4,14},{5,8},{6,7},{6,8},{7,9},{7,10},{8,11},{9,12},{10,11},{10,13},{11,14},{12,13},{13,15},{14,15}}} => {5,2,5,2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,13},{4,12},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11},{10,12},{11,13},{12,13}}} => {2,2,4,2}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,9},{4,9},{5,7},{6,7},{7,8},{8,9}}} => {1,4}, new Diagram1 from {3,3,{{0,6},{1,11},{2,13},{3,12},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11},{9,12},{11,13},{12,13}}} => {5,5,2,2}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,13},{4,12},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11},{10,12},{11,13},{12,13}}} => {5,2,2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,14},{3,17},{4,16},{5,13},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11},{10,12},{10,13},{11,14},{11,15},{12,15},{12,16},{13,16},{14,17},{15,17}}} => {2,2,5,5,2,2}, new Diagram1 from {3,3,{{0,5},{1,6},{2,7},{3,7},{4,6},{6,7}}} => {5}, new Diagram1 from {3,3,{{0,1},{2,6},{3,6},{4,7},{5,7},{6,7}}} => {0,5}, new Diagram1 from {3,3,{{0,6},{1,11},{2,11},{3,9},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11}}} => {4,2,2}, new Diagram1 from {3,3,{{0,1},{2,6},{3,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {0,4,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,12},{4,13},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,10},{10,12},{11,13},{12,13}}} => {2,4,1,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,12},{3,17},{4,16},{5,11},{6,7},{6,8},{7,9},{8,10},{8,11},{9,10},{9,12},{10,13},{11,14},{12,15},{13,14},{13,15},{14,16},{15,17},{16,17}}} => {2,5,2,5,2,5}, new Diagram1 from {3,3,{{0,6},{1,6},{2,3},{4,7},{5,7},{6,7}}} => {1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,9},{4,8},{5,6},{6,7},{7,8},{8,9}}} => {2,5}, new Diagram1 from {3,3,{{0,6},{1,7},{2,13},{3,15},{4,12},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10},{9,11},{10,12},{11,13},{11,14},{12,14},{13,15},{14,15}}} => {2,2,5,5,2}, new Diagram1 from {3,3,{{0,6},{1,9},{2,12},{3,13},{4,11},{5,8},{6,7},{6,8},{7,9},{7,10},{8,11},{9,12},{10,12},{10,13},{11,13}}} => {5,2,4,2}, new Diagram1 from {3,3,{{0,6},{1,2},{3,7},{4,7},{5,6},{6,7}}} => {3,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,6},{4,5},{6,7}}} => {4,0}, new Diagram1 from {3,3,{{0,1},{2,5},{3,4}}} => {0,3}, new Diagram1 from {3,3,{{0,6},{1,8},{2,10},{3,11},{4,11},{5,6},{6,7},{7,8},{7,9},{8,10},{9,10},{9,11}}} => {5,2,4}, new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,7},{4,8},{5,8},{6,7},{6,8},{7,9}}} => {4,1}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,9},{4,9},{5,8},{6,7},{7,8},{8,9}}} => {1,3,2},
	-- now the weird ones
	new Diagram1 from {3,3,{{0,6},{1,6},{2,6},{3,7},{4,7},{5,7}}} => {6},
	new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,8},{4,9},{5,9},{6,7},{7,8},{7,9}}} => {7},
	new Diagram1 from {3,3,{{0,6},{1,8},{2,8},{3,9},{4,9},{5,6},{6,7},{7,8},{7,9}}} => {8},
	new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,7},{4,6},{5,6}}} => {9},
	new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,7},{4,7},{5,6}}} => {10},
	new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,11},{4,11},{5,9},{6,7},{7,8},{7,9},{8,10},{9,10},{10,11}}} => {11},
	new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,10},{4,11},{5,11},{6,7},{6,8},{7,9},{7,10},{8,10},{8,11}}} => {12},
	new Diagram1 from {3,3,{{0,6},{1,8},{2,11},{3,11},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,10},{10,11}}} => {13}
	},
    true => new HashTable from {
	-- The remaining 101 basis diagrams are completed below.
	new Diagram1 from {3,3,{{0,5},{1,6},{2,7},{3,9},{4,8},{6,7},{6,8},{7,9},{8,9}}} => {9,9}, new Diagram1 from {3,3,{{1,6},{3,6},{4,6}}} => {22,7}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,6},{6,7}}} => {28,5,16}, new Diagram1 from {3,3,{{0,6},{1,6},{4,7},{5,7},{6,7}}} => {27,8}, new Diagram1 from {3,3,{{0,6},{1,7},{2,8},{3,9},{4,9},{5,6},{6,7},{7,8},{8,9}}} => {3,28,14}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,8},{4,8},{6,7},{7,8}}} => {9,11,7}, new Diagram1 from {3,3,{{1,2},{3,6},{4,6},{5,6}}} => {21,19,25}, new Diagram1 from {3,3,{{0,6},{1,7},{2,8},{3,8},{5,6},{6,7},{7,8}}} => {3,28}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,7},{4,5},{6,7}}} => {9,11,29}, new Diagram1 from {3,3,{{1,6},{2,8},{3,8},{4,7},{5,6},{6,7},{7,8}}} => {25,9}, new Diagram1 from {3,3,{{1,6},{2,9},{3,9},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10}}} => {25,9,3}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{8,9},{9,10},{10,11}}} => {3,3,9}, new Diagram1 from {3,3,{{0,6},{2,6},{3,7},{4,7},{6,7}}} => {5,16,7}, new Diagram1 from {3,3,{{0,6},{1,9},{2,9},{3,8},{4,7},{5,6},{6,7},{7,8},{8,9}}} => {28,14,3}, new Diagram1 from {3,3,{{0,5},{3,4}}} => {0}, new Diagram1 from {3,3,{{0,6},{2,7},{4,7},{5,6},{6,7}}} => {2,12}, new Diagram1 from {3,3,{{1,6},{2,6},{3,7},{5,7},{6,7}}} => {16,7,13}, new Diagram1 from {3,3,{{0,6},{1,8},{2,8},{4,7},{5,6},{6,7},{7,8}}} => {28,2,12}, new Diagram1 from {3,3,{{0,6},{1,6},{2,6},{4,5}}} => {10,21,17}, new Diagram1 from {3,3,{{0,6},{2,9},{3,9},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10}}} => {14,3,3}, new Diagram1 from {3,3,{{0,5},{1,2}}} => {4}, new Diagram1 from {3,3,{{0,4},{2,3}}} => {5}, new Diagram1 from {3,3,{{0,6},{2,6},{5,6}}} => {2,27,23}, new Diagram1 from {3,3,{{0,5},{1,3}}} => {6}, new Diagram1 from {3,3,{{0,5},{1,4}}} => {6,2}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,10},{4,9},{6,7},{7,8},{7,9},{8,10},{9,10}}} => {10,1,1}, new Diagram1 from {3,3,{{0,2},{4,5}}} => {2,24,17}, new Diagram1 from {3,3,{{0,1},{2,6},{3,6},{5,6}}} => {11,7,13}, new Diagram1 from {3,3,{{0,5},{1,6},{3,6},{4,6}}} => {6,14}, new Diagram1 from {3,3,{{0,6},{1,8},{2,10},{3,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,10}}} => {9,3,28}, new Diagram1 from {3,3,{{2,6},{3,6},{4,6}}} => {7}, new Diagram1 from {3,3,{{2,6},{3,7},{4,7},{5,6},{6,7}}} => {7,13,14}, new Diagram1 from {3,3,{{0,6},{1,6},{2,3},{5,6}}} => {10,13}, new Diagram1 from {3,3,{{0,3},{1,2}}} => {4,0,11}, new Diagram1 from {3,3,{{0,1},{2,6},{3,6},{4,7},{5,7},{6,7}}} => {11,7,25}, new Diagram1 from {3,3,{{0,6},{2,6},{3,6}}} => {5,16}, new Diagram1 from {3,3,{{0,1},{3,4}}} => {24,19}, new Diagram1 from {3,3,{{0,1},{3,5}}} => {24,17,6}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,10},{4,8},{6,7},{6,8},{7,9},{8,10},{9,10}}} => {9,10,1}, new Diagram1 from {3,3,{{0,6},{1,7},{3,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {12,12,6}, new Diagram1 from {3,3,{{0,6},{1,2},{4,6},{5,6}}} => {4,26,8}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{4,6},{6,7}}} => {3,4,26}, new Diagram1 from {3,3,{{1,6},{2,7},{3,9},{4,10},{5,8},{6,7},{6,8},{7,9},{8,10},{9,10}}} => {1,25,9}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,8},{4,7},{6,7},{7,8}}} => {10,1}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,9},{4,8},{5,6},{6,7},{7,8},{8,9}}} => {3,9}, new Diagram1 from {3,3,{{0,6},{1,7},{2,10},{3,10},{4,8},{6,7},{6,8},{7,9},{8,9},{9,10}}} => {3,9,10}, new Diagram1 from {3,3,{{1,6},{2,6},{4,7},{5,7},{6,7}}} => {16,20,8}, new Diagram1 from {3,3,{{0,6},{1,7},{3,8},{4,8},{5,6},{6,7},{7,8}}} => {12,6,14}, new Diagram1 from {3,3,{{1,5},{3,4}}} => {23,0}, new Diagram1 from {3,3,{{0,1},{2,3},{4,5}}} => {11,29}, new Diagram1 from {3,3,{{1,6},{2,6},{5,6}}} => {25,4}, new Diagram1 from {3,3,{{0,6},{2,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {2,12,12}, new Diagram1 from {3,3,{{0,6},{1,6},{3,6},{4,5}}} => {27,22,29}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{7,10},{8,10},{9,11}}} => {9,3,3}, new Diagram1 from {3,3,{{0,5},{2,6},{3,6},{4,6}}} => {14}, new Diagram1 from {3,3,{{1,4},{2,3}}} => {13,5}, new Diagram1 from {3,3,{{0,6},{3,6},{5,6}}} => {0,10,13}, new Diagram1 from {3,3,{{1,6},{3,7},{4,7},{5,6},{6,7}}} => {8,6,14}, new Diagram1 from {3,3,{{1,2},{4,5}}} => {21,17}, new Diagram1 from {3,3,{{0,4},{1,6},{2,6},{3,6}}} => {28,5}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,7},{6,7}}} => {9,11}, new Diagram1 from {3,3,{{0,1},{2,6},{4,6},{5,6}}} => {11,20,8}, new Diagram1 from {3,3,{{0,6},{1,9},{2,11},{3,10},{4,7},{5,6},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {9,9,3}, new Diagram1 from {3,3,{{2,6},{3,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {7,25,9}, new Diagram1 from {3,3,{{1,6},{2,6},{3,6}}} => {16}, new Diagram1 from {3,3,{{4,5}}} => {17}, new Diagram1 from {3,3,{{0,6},{2,7},{3,7},{4,8},{5,8},{6,7},{6,8}}} => {5,1,25}, new Diagram1 from {3,3,{{1,6},{2,7},{3,8},{4,8},{5,6},{6,7},{7,8}}} => {1,13,14}, new Diagram1 from {3,3,{{0,6},{1,7},{3,7},{4,6},{6,7}}} => {6,5,1}, new Diagram1 from {3,3,{{0,5},{1,4},{2,3}}} => {18}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,11},{4,10},{5,6},{6,7},{7,8},{8,9},{8,10},{9,11},{10,11}}} => {3,9,9}, new Diagram1 from {3,3,{{1,6},{2,6},{3,4},{5,6}}} => {25,4,0}, new Diagram1 from {3,3,{{0,6},{1,8},{2,9},{3,9},{4,7},{5,6},{6,7},{7,8},{8,9}}} => {9,3}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,8},{5,7},{6,7},{7,8}}} => {10,1,13}, new Diagram1 from {3,3,{{2,3}}} => {20,22}, new Diagram1 from {3,3,{{2,4}}} => {20}, new Diagram1 from {3,3,{{0,6},{1,3},{4,6},{5,6}}} => {6,5,25}, new Diagram1 from {3,3,{{2,5}}} => {20,23}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{5,6},{6,7}}} => {3,4}, new Diagram1 from {3,3,{{0,6},{2,6},{4,7},{5,7},{6,7}}} => {2,27,8}, new Diagram1 from {3,3,{{0,6},{1,7},{2,8},{4,8},{5,6},{6,7},{7,8}}} => {3,28,2}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,7},{4,6},{5,6}}} => {28,5,25}, new Diagram1 from {3,3,{{0,1}}} => {24}, new Diagram1 from {3,3,{{0,6},{1,7},{2,3},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {3,3}, new Diagram1 from {3,3,{{0,2}}} => {2,24}, new Diagram1 from {3,3,{{0,3}}} => {0,11}, new Diagram1 from {3,3,{{0,4}}} => {26}, new Diagram1 from {3,3,{{0,5}}} => {26,23}, new Diagram1 from {3,3,{{2,5},{3,4}}} => {20,23,0}, new Diagram1 from {3,3,{{0,6},{1,6},{4,6}}} => {27}, new Diagram1 from {3,3,{{0,6},{2,6},{3,6},{4,5}}} => {5,16,29}, new Diagram1 from {3,3,{{0,6},{3,7},{4,7},{5,6},{6,7}}} => {0,3}, new Diagram1 from {3,3,{{1,6},{3,6},{5,6}}} => {8,6}, new Diagram1 from {3,3,{{1,6},{2,7},{3,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {1,1,13}, new Diagram1 from {3,3,{{2,6},{3,6},{4,7},{5,7},{6,7}}} => {7,25}, new Diagram1 from {3,3,{{0,5},{1,6},{2,6},{3,6}}} => {28}, new Diagram1 from {3,3,{{0,1},{3,6},{4,6},{5,6}}} => {24,19,25}, new Diagram1 from {3,3,{{0,6},{4,6},{5,6}}} => {26,8}, new Diagram1 from {3,3,{{0,6},{2,8},{3,8},{4,7},{5,6},{6,7},{7,8}}} => {14,3}, new Diagram1 from {3,3,{{0,6},{1,6},{2,6}}} => {10,21}, new Diagram1 from {3,3,{{0,6},{1,7},{2,7},{3,4},{5,6},{6,7}}} => {3,4,0}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{3,7},{4,7},{5,6}}} => {10,13,14}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{4,7},{6,7}}} => {9,11,20}, new Diagram1 from {3,3,{{1,6},{2,6},{3,7},{4,8},{5,8},{6,7},{7,8}}} => {16,7,25}, new Diagram1 from {3,3,{{0,6},{1,2},{3,6},{4,6}}} => {4,0,10}, new Diagram1 from {3,3,{{0,6},{1,7},{3,7},{5,6},{6,7}}} => {12,6}, new Diagram1 from {3,3,{{0,6},{2,3},{4,6},{5,6}}} => {5,25}, new Diagram1 from {3,3,{{0,6},{1,8},{2,8},{3,7},{4,6},{6,7},{7,8}}} => {28,5,1}, new Diagram1 from {3,3,{{1,6},{2,7},{3,7},{4,6},{6,7}}} => {1}, new Diagram1 from {3,3,{{0,5},{2,3}}} => {2,6}, new Diagram1 from {3,3,{{0,6},{1,8},{2,10},{3,9},{4,6},{6,7},{7,8},{7,9},{8,10},{9,10}}} => {9,9,10}, new Diagram1 from {3,3,{{0,5},{2,4}}} => {2}, new Diagram1 from {3,3,{{0,3},{4,5}}} => {0,11,29}, new Diagram1 from {3,3,{{0,6},{1,7},{2,3},{4,7},{5,6},{6,7}}} => {3}, new Diagram1 from {3,3,{{1,6},{2,8},{3,10},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,10}}} => {25,9,9}, new Diagram1 from {3,3,{{0,6},{1,8},{2,10},{3,11},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,11},{10,11}}} => {9,3,9}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {3,3,4}, new Diagram1 from {3,3,{{1,6},{2,7},{3,9},{4,8},{6,7},{6,8},{7,9},{8,9}}} => {1,1}, new Diagram1 from {3,3,{{0,6},{1,6},{2,6},{3,4}}} => {10,21,19}, new Diagram1 from {3,3,{{2,6},{3,6},{5,6}}} => {7,13}, new Diagram1 from {3,3,{{1,6},{3,6},{4,7},{5,7},{6,7}}} => {22,7,25}, new Diagram1 from {3,3,{{0,6},{1,6},{2,4},{5,6}}} => {10,13,2}, new Diagram1 from {3,3,{{0,4},{1,2}}} => {4,26}, new Diagram1 from {3,3,{{0,4},{1,3}}} => {6,5}, new Diagram1 from {3,3,{{0,6},{2,6},{4,6}}} => {2,27}, new Diagram1 from {3,3,{{0,2},{3,4}}} => {2,24,19}, new Diagram1 from {3,3,{{0,6},{1,6},{2,8},{3,8},{4,9},{5,9},{6,7},{7,8},{7,9}}} => {10,1,25}, new Diagram1 from {3,3,{{0,1},{4,5}}} => {24,17}, new Diagram1 from {3,3,{{1,6},{4,6},{5,6}}} => {8}, new Diagram1 from {3,3,{{0,1},{2,6},{3,6},{4,6}}} => {11,7}, new Diagram1 from {3,3,{{0,6},{2,8},{3,10},{4,9},{5,6},{6,7},{7,8},{7,9},{8,10},{9,10}}} => {14,3,9}, new Diagram1 from {3,3,{{0,5},{1,6},{2,7},{3,7},{4,6},{6,7}}} => {9}, new Diagram1 from {3,3,{{0,6},{1,6},{3,7},{4,7},{6,7}}} => {27,22,7}, new Diagram1 from {3,3,{{1,5},{2,6},{3,6},{4,6}}} => {13,14}, new Diagram1 from {3,3,{{0,6},{1,6},{2,3},{4,6}}} => {10}, new Diagram1 from {3,3,{{0,1},{2,3}}} => {11}, new Diagram1 from {3,3,{{0,6},{1,6},{2,3},{4,7},{5,7},{6,7}}} => {10,25}, new Diagram1 from {3,3,{{0,6},{1,6},{2,7},{5,7},{6,7}}} => {10,25,4}, new Diagram1 from {3,3,{{0,1},{2,4}}} => {11,20}, new Diagram1 from {3,3,{{0,1},{2,5}}} => {11,20,23}, new Diagram1 from {3,3,{{0,6},{1,7},{4,7},{5,6},{6,7}}} => {12}, new Diagram1 from {3,3,{{0,6},{1,2},{3,7},{4,7},{5,6},{6,7}}} => {4,0,3}, new Diagram1 from {3,3,{{0,6},{2,7},{3,7},{4,6},{6,7}}} => {5,1}, new Diagram1 from {3,3,{{0,6},{1,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {12,12}, new Diagram1 from {3,3,{{0,6},{1,7},{2,11},{3,11},{4,10},{5,8},{6,7},{6,8},{7,9},{8,10},{9,10},{9,11}}} => {3,9,3}, new Diagram1 from {3,3,{{1,6},{2,7},{3,7},{5,6},{6,7}}} => {1,13}, new Diagram1 from {3,3,{{0,6},{3,6},{4,7},{5,7},{6,7}}} => {0,10,25}, new Diagram1 from {3,3,{{1,5},{2,3}}} => {13}, new Diagram1 from {3,3,{{1,5},{2,4}}} => {13,2}, new Diagram1 from {3,3,{{1,3},{4,5}}} => {22,29}, new Diagram1 from {3,3,{{1,6},{2,6},{4,6}}} => {16,20}, new Diagram1 from {3,3,{{0,6},{1,7},{2,10},{3,10},{5,8},{6,7},{6,8},{7,9},{8,9},{9,10}}} => {3,3,28}, new Diagram1 from {3,3,{{2,6},{4,6},{5,6}}} => {20,8}, new Diagram1 from {3,3,{{0,6},{3,7},{4,9},{5,8},{6,7},{6,8},{7,9},{8,9}}} => {0,3,3}, new Diagram1 from {3,3,{{0,6},{1,6},{3,4},{5,6}}} => {27,23,0}, new Diagram1 from {3,3,{}} => {15}, new Diagram1 from {3,3,{{0,6},{1,6},{2,9},{3,9},{4,8},{5,7},{6,7},{7,8},{8,9}}} => {10,25,9}, new Diagram1 from {3,3,{{0,6},{3,6},{4,6}}} => {0,10}, new Diagram1 from {3,3,{{1,6},{2,6},{3,6},{4,5}}} => {16,29}, new Diagram1 from {3,3,{{1,2},{3,4}}} => {21,19}, new Diagram1 from {3,3,{{1,2},{3,5}}} => {21,17,6}, new Diagram1 from {3,3,{{3,4}}} => {19}, new Diagram1 from {3,3,{{0,6},{1,6},{3,7},{5,7},{6,7}}} => {27,8,6}, new Diagram1 from {3,3,{{3,5}}} => {17,6}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,9},{4,8},{5,8},{6,7},{6,8},{7,9}}} => {9,10,25}, new Diagram1 from {3,3,{{0,6},{1,7},{2,8},{3,8},{4,6},{6,7},{7,8}}} => {9,10}, new Diagram1 from {3,3,{{0,6},{2,7},{3,9},{4,8},{6,7},{6,8},{7,9},{8,9}}} => {5,1,1}, new Diagram1 from {3,3,{{1,6},{2,7},{3,7},{4,8},{5,8},{6,7},{6,8}}} => {1,25}, new Diagram1 from {3,3,{{0,5},{1,2},{3,4}}} => {4,0}, new Diagram1 from {3,3,{{1,6},{2,6},{3,7},{4,7},{6,7}}} => {16,7}, new Diagram1 from {3,3,{{1,2}}} => {21}, new Diagram1 from {3,3,{{1,3}}} => {22}, new Diagram1 from {3,3,{{1,4}}} => {22,20}, new Diagram1 from {3,3,{{1,5}}} => {23}, new Diagram1 from {3,3,{{0,6},{1,6},{5,6}}} => {27,23}, new Diagram1 from {3,3,{{0,6},{1,7},{2,9},{3,8},{6,7},{6,8},{7,9},{8,9}}} => {9,9,11}, new Diagram1 from {3,3,{{0,6},{2,7},{3,7},{5,6},{6,7}}} => {2,12,6}, new Diagram1 from {3,3,{{1,6},{2,3},{4,6},{5,6}}} => {25}, new Diagram1 from {3,3,{{1,6},{2,7},{4,7},{5,6},{6,7}}} => {1,13,2}, new Diagram1 from {3,3,{{0,6},{1,8},{3,8},{4,7},{5,6},{6,7},{7,8}}} => {6,14,3}, new Diagram1 from {3,3,{{0,5},{1,6},{2,6},{4,6}}} => {28,2}, new Diagram1 from {3,3,{{1,6},{2,7},{3,9},{4,10},{5,10},{6,7},{6,8},{7,9},{8,9},{8,10}}} => {1,1,25}, new Diagram1 from {3,3,{{0,6},{1,6},{3,6}}} => {27,22}, new Diagram1 from {3,3,{{0,5},{1,6},{2,6},{3,7},{4,7},{6,7}}} => {28,14}, new Diagram1 from {3,3,{{2,3},{4,5}}} => {29}, new Diagram1 from {3,3,{{3,6},{4,6},{5,6}}} => {19,25}
	}
    }
gens3:=new HashTable from {
    false => fulllst33_{16, 36, 62, 15, 37, 61, 0, 26, 27, 28, 29, 40, 49, 67},
    true => lst33_{158,140,169,62,239,183,212,108,119,61,273,267,207,131,146,111,136,109,63,104,103,130,122,117,211,81,164,210,254,97}
}
-- Store each decomposition as a sum of {coefficient, generator word} pairs.
-- This also permits the linear combination needed for basis diagram 67.
decTable = new HashTable from apply(pairs decTable,(dilute,tab)->
    dilute => new HashTable from apply(pairs tab,(d,word)->d=>{{1_F,word}}))
completeDiluteDecompositions := () -> (
    tab := new MutableHashTable from pairs decTable#true;
    recipes := myget "decompositions3dilute.m2";
    extend := i -> (
        d := lst33#i;
        if tab#?d then return tab#d;
        spec := recipes#i;
        terms := extend(spec#0);
        tab#d = apply(terms,t->{t#0/ϕ^(spec#3),
            if spec#2 then prepend(spec#1,t#1) else append(t#1,spec#1)})
        );
    scan(keys recipes,extend);
    -- H_1^2 H_2^2 H_1^2 is already the diagram, without a scalar factor.
    tab#(lst33#79) = {{1_F,{3,3,9,9,3,3}}};
    -- The square/pentagon relation expresses diagram 65 times H_2 as a
    -- linear combination containing diagram 67 and already covered diagrams.
    relation := skein(lst33#65 | (gens3#true)#9,5);
    leading := relation_(lst33#67);
    if leading==0 then error "rep: singular parameters in the dilute decomposition of diagram 67; compute generically before specialising";
    terms := apply(tab#(lst33#65),t->{t#0/leading,append(t#1,9)});
    scan(pairs relation,(d,c)->if d!=lst33#67 then
        terms=terms|apply(tab#d,t->{-c*t#0/leading,t#1}));
    tab#(lst33#67) = terms;
    new HashTable from pairs tab
    )
decTable = new HashTable from {false=>decTable#false,true=>completeDiluteDecompositions()}
decompose Diagram1 := {Dilute => null} >> o -> d -> (
    dilute:=if o.Dilute===null then partial d else o.Dilute;
    if decTable#dilute#?d then new Sum from apply(decTable#dilute#d,
        t->new Product from prepend(t#0,(gens3#dilute)_(t#1))) else d
    )
decompose Diagram := {Dilute => null} >> o -> d -> (
    dilute := if o.Dilute === null then any(keys d,partial) else o.Dilute;
    applyKeys(d,x->decompose(x,Dilute=>dilute))
    )

-- representations of Hom(2) and Hom^dilute(2): just go thru every diagram... see diagrams-rep.m2
reps2=myget "reps2.m2"
reps2=apply(#reps2,i->apply(5,j->(scale fulllst2#j)^-1*reps2#i#j))
reps2dilute=myget "reps2dilute.m2"
reps2dilute=apply(#reps2dilute,i->apply(16,j->(scale lst2#j)^-1*reps2dilute#i#j))

loadrep3 = memoize((n,dilute)->( -- TODO dilute
	try factored(R,true);
	l:=myget ("reps3"|(if dilute then "dilute" else "")|"_"|toString n|".m2");
	try factored(R,false);
	apply(#l,j->(scale (gens3#dilute)#j)^-1*l#j)
	))

-- A zero Diagram has no boundary metadata. Strands and Dilute make its
-- representation unambiguous without changing the Diagram data structure.
repContext := (d,o) -> (
    if #d==0 then (
        if o.Strands===null or o.Dilute===null then
            error "rep: a zero diagram requires Strands=>2 or 3 and Dilute=>true or false";
        ) else (
        if any(keys d,x->x#0!=x#1) then error "rep: only applies to endomorphisms";
        );
    k := if #d==0 then o.Strands else (first keys d)#0;
    if k!=2 and k!=3 then error "rep: only two or three strands are implemented";
    if #d>0 and any(keys d,x->x#0!=k) then error "rep: inconsistent boundary sizes";
    if o.Strands=!=null and o.Strands!=k then error "rep: Strands disagrees with the diagram";
    dilute := if o.Dilute===null then any(keys d,partial) else o.Dilute;
    if dilute=!=true and dilute=!=false then error "rep: Dilute must be true, false, or null";
    if not dilute and any(keys d,partial) then error "rep: partial diagrams require Dilute=>true";
    (k,dilute)
    )
repTop := (k,n) -> (k==2 and n>=2) or (k==3 and n>=5)
repData := (k,n,dilute) -> (
    if n<0 or n>=(if k==2 then 5 else 11) then error "rep: representation index out of range";
    if repTop(k,n) then dilute=false;
    if k==2 then (if dilute then reps2dilute else reps2)#n else loadrep3(n,dilute)
    )
repKnown := (k,n,dilute,d) -> (
    -- Partial diagrams belong to the ideal killed by the top representations.
    if dilute and repTop(k,n) and partial d then true else (
        if repTop(k,n) then dilute=false;
        if k==2 then member(d,if dilute then lst2 else fulllst2) else decTable#dilute#?d
        )
    )
repBasis := memoize((k,n,dilute,d) -> (
    l := repData(k,n,dilute);
    unit := id_(F^(numRows first l));
    if dilute and repTop(k,n) and partial d then return 0*unit;
    if repTop(k,n) then dilute=false;
    if not repKnown(k,n,dilute,d) then
        error("rep: no decomposition for "|toString d|" in representation "|toString n|", Dilute=>"|toString dilute);
    if k==2 then return sub(l#(position(if dilute then lst2 else fulllst2,x->x==d)),F);
    result := 0*unit;
    scan(decTable#dilute#d,t->(
        word := unit;
        scan(t#1,i->word=word*l#i);
        result=result+t#0*word;
        ));
    result
    ))
rep=method(Options => {Dilute => null, Strands => null}, TypicalValue => Matrix)
rep(ZZ,Diagram) := o -> (n,d) -> (
    (k,dilute) := repContext(d,o);
    l := repData(k,n,dilute);
    result := 0*id_(F^(numRows first l));
    scan(pairs d,(dd,coefficient)->(
        if repKnown(k,n,dilute,dd) then result=result+coefficient*repBasis(k,n,dilute,dd)
        else (
            -- Reduce an arbitrary input, but never discard an unsupported term.
            if member(dd,if k==2 then lst2 else lst33) then
                error("rep: no decomposition for "|toString dd|" in representation "|toString n);
            reduced := skein(dd,5);
            if k==3 and any(keys reduced,term->not repKnown(k,n,dilute,term)) then
                reduced=skein(reduced,6);
            scan(pairs reduced,(term,c)->result=result+coefficient*c*repBasis(k,n,dilute,term));
            );
        ));
    result
    )
rep(ZZ,Diagram1) := o -> (n,d) -> rep(n,diagram d,Dilute=>o.Dilute,Strands=>o.Strands)
rep Diagram := o -> d -> (
    (k,dilute) := repContext(d,o);
    directSum apply(if k==2 then 5 else 11,i->rep(i,d,Dilute=>dilute,Strands=>k))
    )
rep Diagram1 := o -> d -> rep(diagram d,Dilute=>o.Dilute,Strands=>o.Strands)

blockMatrixForm=true

beginDocumentation()

-- Keep package checks short; the exhaustive multiplication and spectral
-- Yang--Baxter suites live in tests/exceptional-diagrams.m2.
TEST ///
-- Full bar involution, including the spectral variables.
if (options ExceptionalDiagrams).Configuration#"parameters" == "generic" then (
    assert(bar p==1/p and bar q==1/q and bar u==1/u and bar v==1/v);
    assert(bar 0==0 and bar 1==1);
    edTestScalar=(p+u*q)/(v+p*q);
    assert(bar(bar edTestScalar)==edTestScalar);
    edTestR=Rmatrix();
    assert(bar edTestR==edTestR);
    edTestMatrix=rep edTestR;
    assert(bar edTestMatrix==edTestMatrix and bar(bar edTestMatrix)==edTestMatrix);
    edTestBraid=braid(Dilute=>true);
    assert(edTestBraid*bar edTestBraid==diagramId(2,Dilute=>true));
    ) else assert(try (bar(Rmatrix()); false) else true);
///

TEST ///
-- Identities and zeros must have the correct matrix dimensions.
scan({2,3},k->scan({false,true},dilute->(
    edTestDiagram:=diagramId(k,Dilute=>dilute);
    zz:=edTestDiagram-edTestDiagram;
    scan(0..(if k==2 then 4 else 10),i->(
        edTestMatrix:=rep(i,edTestDiagram,Dilute=>dilute);
        assert(instance(edTestMatrix,Matrix) and edTestMatrix==id_(source edTestMatrix));
        zm:=rep(i,zz,Strands=>k,Dilute=>dilute);
        assert(instance(zm,Matrix) and numRows zm==numRows edTestMatrix and zm==0*edTestMatrix);
        ));
    edTestMatrix:=rep(edTestDiagram,Dilute=>dilute);
    assert(edTestMatrix==id_(source edTestMatrix));
    assert(rep(zz,Strands=>k,Dilute=>dilute)==0*edTestMatrix);
    )));
///

TEST ///
-- Unsupported inputs must report errors instead of silently returning zero.
edTestFails = edTestScalar -> try (edTestScalar(); false) else true;
assert(edTestFails(()->rep(diagramId(3)-diagramId(3))));
assert(edTestFails(()->rep(diagramId(3),Strands=>2)));
assert(edTestFails(()->rep(11,diagramId(3))));
assert(edTestFails(()->rep(diagramId(4))));
assert(edTestFails(()->rep(diagram(2,3,{}))));
assert(edTestFails(()->rep(diagramId(2)+diagramId(3))));
assert(edTestFails(()->rep(diagram(2,2,{{0,2},{1,3}}))));
///

TEST ///
-- Dilute option forwarding and the formerly missing nonzero diagram.
edTestInput=(braid())_1;
edTestMatrix=rep(edTestInput,Dilute=>true);
assert(edTestMatrix==directSum apply(11,i->rep(i,edTestInput,Dilute=>true)));
assert(numRows edTestMatrix==45 and numRows rep(edTestInput,Dilute=>false)==26);
edTestDiagram=diagram(3,3,{{0,6},{1,6},{2,6},{3,7},{4,7},{5,7}});
edTestMatrix=rep(0,edTestDiagram,Dilute=>true);
edTestOrdinary=rep(0,edTestDiagram,Dilute=>false);
assert(numRows edTestMatrix==5 and edTestMatrix_(0,0)==edTestOrdinary_(0,0) and edTestMatrix_(0,0)!=0);
-- Use the I representation: unlike top representations, it cannot discard
-- all partial diagrams by the cut-length quotient.
edTestBasis=diagramList(3,3,Dilute=>true);
assert(#edTestBasis==287);
scan(edTestBasis,d->assert(instance(rep(0,d,Dilute=>true),Matrix)));
edTestPartial=diagram(3,3,{{0,5},{1,4}});
scan(5..10,i->(
    zm:=rep(i,edTestPartial,Dilute=>true);
    assert(instance(zm,Matrix) and zm==0*zm);
    ));
///

TEST ///
-- Braid relation in all eleven dilute irreducible representations.
edTestBraid=braid(Dilute=>true);
scan(0..10,i->(
    s1:=rep(i,edTestBraid_1); s2:=rep(i,edTestBraid_2);
    assert(s1*s2*s1==s2*s1*s2);
    ));
///
