-- Run from any directory: M2 --script exceptional-diagrams.m2 paper generic
-- Optional suites: "multiplication" (allrandom) or "ybe" (random or generic).
-- The basic suite can run one group per worker: recipes, context, restrictions,
-- identities. For restrictions, a fifth argument selects an index 0..4.
-- A sixth argument 0..3 selects a range of 20 of the 80 ordinary diagrams.
edArgs = drop(scriptCommandLine,1);
edAlpha = if #edArgs>0 then edArgs#0 else "paper";
edParameters = if #edArgs>1 then edArgs#1 else "generic";
edSuite = if #edArgs>2 then edArgs#2 else "basic";
edStage = if #edArgs>3 then edArgs#3 else "all";
edIndex = if #edArgs>4 then value edArgs#4 else null;
edChunk = if #edArgs>5 then value edArgs#5 else null;
assert(member(edStage,{"all","recipes","context","restrictions","identities"}));
assert(edStage=="all" or edSuite=="basic");
assert(edIndex===null or (edStage=="restrictions" and member(edIndex,toList(0..4))));
assert(edChunk===null or (edStage=="restrictions" and member(edChunk,toList(0..3))));
setRandomSeed 260106;
needsPackage("ExceptionalDiagrams",FileName=>currentFileDirectory|"../ExceptionalDiagrams.m2",
    Configuration=>{"alpha"=>edAlpha,"parameters"=>edParameters});
debug ExceptionalDiagrams;
edPass = msg -> (print("PASS "|msg); flush stdio);
edFails = f -> try (f(); false) else true;
-- Compare coefficients in F: specialisation can mix F0 and F coefficients.
edDiagramEqual = (x,y) -> all(unique(keys x|keys y),d->sub(x_d,F)==sub(y_d,F));
edGenerators = lst33_{158,140,169,62,239,183,212,108,119,61,273,267,207,131,146,111,136,109,63,104,103,130,122,117,211,81,164,210,254,97};
if member(edStage,{"all","recipes"}) then (
assert(all(lst33,d->decTable#true#?d));
assert(all(fulllst33,d->decTable#false#?d));
edPass "complete ordinary and dilute basis coverage";

-- Check every stored recipe diagrammatically, independently of rep.
-- These are identities before specialising p,q, in both normalisations.
edRecipes = value get(currentFileDirectory|"../ExceptionalDiagrams/decompositions3dilute.m2");
scan(pairs edRecipes,(i,spec)->(
    dd:=lst33#(spec#0); gg:=edGenerators#(spec#1);
    assert(edDiagramEqual(skein(if spec#2 then gg|dd else dd|gg,3),ϕ^(spec#3)*lst33#i));
    ));
edRaw79=edGenerators#3|edGenerators#3|edGenerators#9|edGenerators#9|edGenerators#3|edGenerators#3;
assert(edDiagramEqual(skein(edRaw79,3),diagram(lst33#79)));
-- Check that diagram 67's completed word sum reproduces its defining relation.
edRelation=skein(lst33#65|edGenerators#9,5);
assert(edRelation_(lst33#67)!=0);
assert(all(keys edRelation,d->member(d,lst33)));
edPass "100 product decompositions and the square/pentagon relation";
);

if member(edStage,{"all","context"}) then (
scan({2,3},k->scan({false,true},dilute->(
    dd:=diagramId(k,Dilute=>dilute);
    zz:=dd-dd;
    scan(0..(if k==2 then 4 else 10),i->(
        mm:=rep(i,dd,Dilute=>dilute);
        assert(instance(mm,Matrix));
        assert(mm==id_(source mm));
        zm:=rep(i,zz,Strands=>k,Dilute=>dilute);
        assert(instance(zm,Matrix) and numRows zm==numRows mm and zm==0*mm);
        ));
    mm:=rep(dd,Dilute=>dilute);
    assert(mm==id_(source mm));
    assert(rep(zz,Strands=>k,Dilute=>dilute)==0*mm);
    )));
assert(edFails(()->rep(diagramId(3)-diagramId(3))));
assert(edFails(()->rep(diagramId(3),Strands=>2)));
assert(edFails(()->rep(11,diagramId(3))));
assert(edFails(()->rep(diagramId(4))));
assert(edFails(()->rep(diagram(2,3,{}))));
assert(edFails(()->rep(diagramId(2)+diagramId(3))));
assert(edFails(()->rep(diagram(2,2,{{0,2},{1,3}}))));
edPass "identity and zero matrix sizes; invalid-context errors";

edX=(braid())_1;
edExplicit=directSum apply(11,i->rep(i,edX,Dilute=>true));
assert(rep(edX,Dilute=>true)==edExplicit);
assert(numRows edExplicit==45);
assert(numRows rep(edX,Dilute=>false)==26);
-- Diagram1 and Diagram must choose the same algebra and representation.
scan(0..10,i->assert(rep(i,edGenerators#2)==rep(i,diagram(edGenerators#2))));
scan(5..10,i->(mm:=rep(i,edGenerators#2,Dilute=>true); assert(mm==0*mm)));
edD=diagram(3,3,{{0,6},{1,6},{2,6},{3,7},{4,7},{5,7}});
edM=rep(0,edD,Dilute=>true);
edOrdinary=rep(0,edD,Dilute=>false);
assert(edM_(0,0)==edOrdinary_(0,0) and edM_(0,0)!=0);
assert(numRows edM==5);
edPass "option forwarding, quotient zeros, and the formerly missing nonzero diagram";
);

-- Fully occupied diagrams act in the ordinary summand and kill the others.
if member(edStage,{"all","restrictions"}) then (
edRestrictionDiagrams=if edChunk===null then fulllst33 else take(drop(fulllst33,20*edChunk),20);
scan(if edIndex===null then toList(0..4) else {edIndex},n->scan(edRestrictionDiagrams,dd->(
    small:=rep(n,diagram dd,Dilute=>false);
    big:=rep(n,diagram dd,Dilute=>true);
    remaining:=numRows big-numRows small;
    assert(big==directSum(small,map(F^remaining,F^remaining,0)));
    )));
edPass "selected ordinary diagrams restrict correctly in the selected representations";
);

if member(edStage,{"all","identities"}) then (
edS=braid(Dilute=>true);
scan(0..10,i->(
    s1:=rep(i,edS_1); s2:=rep(i,edS_2);
    assert(s1*s2*s1==s2*s1*s2);
    ));
edPass "braid relation in all eleven dilute representations";

if edParameters=="generic" then (
    assert(bar p==1/p and bar q==1/q and bar u==1/u and bar v==1/v);
    assert(bar 0==0 and bar 1==1);
    edF=(p+u*q)/(v+p*q);
    assert(bar(bar edF)==edF);
    edR=Rmatrix();
    assert(bar edR==edR);
    assert(bar(bar edS)==edS);
    assert(edS*bar edS==diagramId(2,Dilute=>true));
    edRM=rep edR;
    assert(bar edRM==edRM and bar(bar edRM)==edRM);
    assert(edRM*sub(edRM,u=>1/u)==id_(source edRM));
    edPass "full bar involution on scalars, diagrams, and matrices; R unitarity";
    ) else (
    assert(edFails(()->bar(Rmatrix())));
    edPass "bar rejects specialised parameters";
    );
);

if edSuite=="multiplication" then (
    -- Explicit full reduction is fast after specialising parameters. These
    -- comparisons do not use the completed decomposition table to reduce products.
    edBasisMatrices=apply(lst33,d->rep(diagram d,Dilute=>true));
    edGeneratorMatrices=apply(edGenerators,d->rep(diagram d,Dilute=>true));
    scan(0..286,i->(
        scan(0..29,j->(
            dd:=skein(lst33#i|edGenerators#j,6);
            assert(rep(dd,Strands=>3,Dilute=>true)==edBasisMatrices#i*edGeneratorMatrices#j);
            ));
        if i%25==0 then edPass("multiplication through basis diagram "|toString i);
        ));
    edPass "all 287 basis diagrams times all 30 generators, in every representation";
    );

if edSuite=="ybe" then (
    edR=Rmatrix();
    scan(reverse toList(0..10),i->(
        r1:=rep(i,edR_1); r2:=rep(i,edR_2);
        -- Symbol keys also work with Factor's finite-field fraction elements,
        -- whose presentation may give a generator a nontrivial unit denominator.
        lhs:=r1*sub(r2,symbol u=>u*v)*sub(r1,symbol u=>v);
        rhs:=sub(r2,symbol u=>v)*sub(r1,symbol u=>u*v)*r2;
        assert(lhs==rhs);
        edPass("spectral Yang--Baxter equation in representation "|toString i);
        ));
    );
edPass("completed "|edAlpha|" / "|edParameters|" / "|edSuite);
