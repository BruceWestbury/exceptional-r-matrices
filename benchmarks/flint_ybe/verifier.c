#define _POSIX_C_SOURCE 200809L
#include <flint/fmpz_mpoly.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
/* Exact rational construction; all YBE products use integer polynomials. */
static fmpz_mpoly_ctx_t ctx ;
static const char * vars [ ] = {
    "p" , "q" , "u" , "v"
}
;
static void die ( const char * s ) {
    fprintf ( stderr , "ERROR: %s\n" , s ) ;
    exit ( 2 ) ;
}
static double now ( void ) {
    struct timespec t ;
    clock_gettime ( CLOCK_MONOTONIC , & t ) ;
    return t . tv_sec + t . tv_nsec * 1e-9 ;
}
typedef struct {
    fmpz_mpoly_t n , d ;
}
Rat ;
static void init ( Rat * r ) {
    fmpz_mpoly_init ( r -> n , ctx ) ;
    fmpz_mpoly_init ( r -> d , ctx ) ;
    fmpz_mpoly_one ( r -> d , ctx ) ;
}
static void clear ( Rat * r ) {
    fmpz_mpoly_clear ( r -> n , ctx ) ;
    fmpz_mpoly_clear ( r -> d , ctx ) ;
}
static void set ( Rat * r , const Rat * a ) {
    fmpz_mpoly_set ( r -> n , a -> n , ctx ) ;
    fmpz_mpoly_set ( r -> d , a -> d , ctx ) ;
}
static void integer ( Rat * r , long x ) {
    fmpz_mpoly_set_si ( r -> n , x , ctx ) ;
    fmpz_mpoly_one ( r -> d , ctx ) ;
}
static void norm ( Rat * r ) {
    if ( fmpz_mpoly_is_zero ( r -> d , ctx ) ) die ( "zero denominator" ) ;
    if ( fmpz_mpoly_is_zero ( r -> n , ctx ) ) {
        fmpz_mpoly_one ( r -> d , ctx ) ;
        return ;
    }
    fmpz_mpoly_t g ;
    fmpz_mpoly_init ( g , ctx ) ;
    if ( ! fmpz_mpoly_gcd ( g , r -> n , r -> d , ctx ) ) die ( "gcd failed" ) ;
    fmpz_mpoly_divexact ( r -> n , r -> n , g , ctx ) ;
    fmpz_mpoly_divexact ( r -> d , r -> d , g , ctx ) ;
    if ( fmpz_sgn ( r -> d -> coeffs ) < 0 ) {
        fmpz_mpoly_neg ( r -> d , r -> d , ctx ) ;
        fmpz_mpoly_neg ( r -> n , r -> n , ctx ) ;
    }
    fmpz_mpoly_clear ( g , ctx ) ;
}
static void op ( Rat * r , const Rat * a , const Rat * b , char c ) {
    Rat t ;
    init ( & t ) ;
    if ( c == '+' || c == '-' ) {
        fmpz_mpoly_t z ;
        fmpz_mpoly_init ( z , ctx ) ;
        fmpz_mpoly_mul ( t . n , a -> n , b -> d , ctx ) ;
        fmpz_mpoly_mul ( z , b -> n , a -> d , ctx ) ;
        if ( c == '+' ) fmpz_mpoly_add ( t . n , t . n , z , ctx ) ;
        else fmpz_mpoly_sub ( t . n , t . n , z , ctx ) ;
        fmpz_mpoly_mul ( t . d , a -> d , b -> d , ctx ) ;
        fmpz_mpoly_clear ( z , ctx ) ;
    }
    else {
        fmpz_mpoly_mul ( t . n , a -> n , c == '*' ? b -> n : b -> d , ctx ) ;
        fmpz_mpoly_mul ( t . d , a -> d , c == '*' ? b -> d : b -> n , ctx ) ;
    }
    norm ( & t ) ;
    set ( r , & t ) ;
    clear ( & t ) ;
}
static void power ( Rat * r , long k ) {
    Rat t ;
    init ( & t ) ;
    if ( ! fmpz_mpoly_pow_ui ( t . n , k < 0 ? r -> d : r -> n , labs ( k ) , ctx ) || ! fmpz_mpoly_pow_ui ( t . d , k < 0 ? r -> n : r -> d , labs ( k ) , ctx ) ) die ( "power" ) ;
    set ( r , & t ) ;
    clear ( & t ) ;
}
/* Small JSON tree reader. Strings used as mathematics must be ASCII without escapes. */
typedef struct J {
    char * s ;
    struct J * * a ;
    int n ;
    char kind ;
}
J ;
static void ws ( const char * * p ) {
    while ( isspace ( ( unsigned char ) * * p ) ) ++ * p ;
}
static J * json ( const char * * p ) {
    ws ( p ) ;
    J * j = calloc ( 1 , sizeof * j ) ;
    j -> kind = * * p ;
    if ( * * p == '[' || * * p == '{' ) {
        char end = * * p == '[' ? ']' : '}' ;
        ++ * p ;
        ws ( p ) ;
        while ( * * p != end ) {
            if ( ! * * p ) die ( "JSON end" ) ;
            j -> a = realloc ( j -> a , ( j -> n + 1 ) * sizeof * j -> a ) ;
            j -> a [ j -> n ++ ] = json ( p ) ;
            ws ( p ) ;
            if ( * * p == ',' || * * p == ':' ) ++ * p ;
            else if ( * * p != end ) die ( "JSON separator" ) ;
            ws ( p ) ;
        }
        ++ * p ;
    }
    else {
        const char * start ;
        if ( * * p == '"' ) {
            start = ++ * p ;
            while ( * * p && * * p != '"' ) {
                if ( * * p == '\\' && ( * p ) [ 1 ] ) ++ * p ;
                ++ * p ;
            }
            j -> s = strndup ( start , * p - start ) ;
            if ( ! * * p ) die ( "JSON string" ) ;
            ++ * p ;
        }
        else {
            start = * p ;
            while ( * * p && ! strchr ( ",]} \n\r\t" , * * p ) ) ++ * p ;
            j -> s = strndup ( start , * p - start ) ;
        }
    }
    return j ;
}
static J * readj ( const char * path ) {
    FILE * f = fopen ( path , "rb" ) ;
    if ( ! f ) die ( path ) ;
    fseek ( f , 0 , SEEK_END ) ;
    long n = ftell ( f ) ;
    rewind ( f ) ;
    char * s = calloc ( n + 1 , 1 ) ;
    if ( fread ( s , 1 , n , f ) != ( size_t ) n ) die ( "read" ) ;
    fclose ( f ) ;
    const char * p = s ;
    J * j = json ( & p ) ;
    ws ( & p ) ;
    if ( * p ) die ( "trailing JSON" ) ;
    free ( s ) ;
    return j ;
}
static J * get ( J * j , const char * key ) {
    if ( ! j || j -> kind != '{' ) die ( "JSON object expected" ) ;
    for ( int i = 0 ; i + 1 < j -> n ; i += 2 ) if ( ! strcmp ( j -> a [ i ] -> s , key ) ) return j -> a [ i + 1 ] ;
    die ( key ) ;
    return NULL ;
}
static int ji ( J * j ) {
    return atoi ( j -> s ) ;
}
static J * defs ;
typedef struct {
    char * name ;
    Rat r ;
}
Binding ;
static Binding env [ 160 ] ;
static int ne ;
static void expr ( Rat * , const char * ) ;
static Rat * lookup ( const char * name ) {
    for ( int i = 0 ; i < ne ; i ++ ) if ( ! strcmp ( name , env [ i ] . name ) ) return & env [ i ] . r ;
    if ( ne == 160 ) die ( "bindings" ) ;
    int i = ne ++ ;
    env [ i ] . name = strdup ( name ) ;
    init ( & env [ i ] . r ) ;
    expr ( & env [ i ] . r , get ( get ( defs , name ) , "expression" ) -> s ) ;
    return & env [ i ] . r ;
}
static void bind ( const char * name , const char * s ) {
    int i = ne ++ ;
    env [ i ] . name = strdup ( name ) ;
    init ( & env [ i ] . r ) ;
    expr ( & env [ i ] . r , s ) ;
}
static void sum ( Rat * , const char * * ) ;
static void atom ( Rat * r , const char * * p ) {
    ws ( p ) ;
    if ( * * p == '+' || * * p == '-' ) {
        char c = * ( * p ) ++ ;
        atom ( r , p ) ;
        if ( c == '-' ) fmpz_mpoly_neg ( r -> n , r -> n , ctx ) ;
        return ;
    }
    if ( * * p == '(' ) {
        ++ * p ;
        sum ( r , p ) ;
        ws ( p ) ;
        if ( * ( * p ) ++ != ')' ) die ( "parenthesis" ) ;
    }
    else if ( isdigit ( ( unsigned char ) * * p ) ) {
        char * e ;
        long k = strtol ( * p , & e , 10 ) ;
        * p = e ;
        integer ( r , k ) ;
    }
    else if ( isalpha ( ( unsigned char ) * * p ) || * * p == '_' ) {
        const char * s = * p ;
        while ( isalnum ( ( unsigned char ) * * p ) || * * p == '_' ) ++ * p ;
        char * id = strndup ( s , * p - s ) ;
        set ( r , lookup ( id ) ) ;
        free ( id ) ;
    }
    else die ( "scalar token" ) ;
    ws ( p ) ;
    if ( * * p == '^' || ( ( * p ) [ 0 ] == '*' && ( * p ) [ 1 ] == '*' ) ) {
        * p += * * p == '^' ? 1 : 2 ;
        ws ( p ) ;
        int par = * * p == '(' ;
        if ( par ) ++ * p ;
        char * e ;
        long k = strtol ( * p , & e , 10 ) ;
        if ( e == * p ) die ( "integer exponent" ) ;
        * p = e ;
        ws ( p ) ;
        if ( par && * ( * p ) ++ != ')' ) die ( "exponent parenthesis" ) ;
        power ( r , k ) ;
    }
}
static void product ( Rat * r , const char * * p ) {
    atom ( r , p ) ;
    ws ( p ) ;
    while ( * * p == '*' || * * p == '/' ) {
        char c = * ( * p ) ++ ;
        Rat b ;
        init ( & b ) ;
        atom ( & b , p ) ;
        op ( r , r , & b , c ) ;
        clear ( & b ) ;
        ws ( p ) ;
    }
}
static void sum ( Rat * r , const char * * p ) {
    product ( r , p ) ;
    ws ( p ) ;
    while ( * * p == '+' || * * p == '-' ) {
        char c = * ( * p ) ++ ;
        Rat b ;
        init ( & b ) ;
        product ( & b , p ) ;
        op ( r , r , & b , c ) ;
        clear ( & b ) ;
        ws ( p ) ;
    }
}
static void expr ( Rat * r , const char * s ) {
    sum ( r , & s ) ;
    ws ( & s ) ;
    if ( * s ) die ( "scalar trailing text" ) ;
}
typedef struct {
    int n ;
    Rat * e ;
}
Mat ;
static Mat mat ( int n , int eye ) {
    Mat m = {
        n , calloc ( n * n , sizeof ( Rat ) )
    }
    ;
    for ( int i = 0 ; i < n * n ; i ++ ) {
        init ( m . e + i ) ;
        if ( eye && i / n == i % n ) integer ( m . e + i , 1 ) ;
    }
    return m ;
}
static void mc ( Mat * m ) {
    for ( int i = 0 ; i < m -> n * m -> n ; i ++ ) clear ( m -> e + i ) ;
    free ( m -> e ) ;
}
static Mat copy ( Mat a ) {
    Mat b = mat ( a . n , 0 ) ;
    for ( int i = 0 ; i < a . n * a . n ; i ++ ) set ( b . e + i , a . e + i ) ;
    return b ;
}
static void addscaled ( Mat a , Mat b , const Rat * s ) {
    Rat t ;
    init ( & t ) ;
    for ( int i = 0 ; i < a . n * a . n ; i ++ ) {
        op ( & t , b . e + i , s , '*' ) ;
        op ( a . e + i , a . e + i , & t , '+' ) ;
    }
    clear ( & t ) ;
}
static Mat mm ( Mat a , Mat b ) {
    int n = a . n ;
    Mat c = mat ( n , 0 ) ;
    Rat t ;
    init ( & t ) ;
    for ( int i = 0 ; i < n ; i ++ ) for ( int k = 0 ; k < n ; k ++ ) if ( ! fmpz_mpoly_is_zero ( a . e [ i * n + k ] . n , ctx ) ) for ( int j = 0 ; j < n ; j ++ ) if ( ! fmpz_mpoly_is_zero ( b . e [ k * n + j ] . n , ctx ) ) {
        op ( & t , a . e + i * n + k , b . e + k * n + j , '*' ) ;
        op ( c . e + i * n + j , c . e + i * n + j , & t , '+' ) ;
    }
    clear ( & t ) ;
    return c ;
}
static void plus ( Mat a , Mat b ) {
    Rat one ;
    init ( & one ) ;
    integer ( & one , 1 ) ;
    addscaled ( a , b , & one ) ;
    clear ( & one ) ;
}
static Mat scaled ( Mat a , const Rat * r ) {
    Mat b = mat ( a . n , 0 ) ;
    addscaled ( b , a , r ) ;
    return b ;
}
static Mat polynomial ( Mat local [ 16 ] , J * ordinary , const char * id ) {
    int n = local [ 0 ] . n ;
    Mat h = scaled ( local [ 3 ] , lookup ( "b11" ) ) , h2 = mm ( h , h ) , k = scaled ( local [ 2 ] , lookup ( "b11" ) ) ;
    J * relations = get ( ordinary , "relations" ) , * terms = NULL ;
    for ( int i = 0 ; i < relations -> n ; i ++ ) if ( ! strcmp ( get ( relations -> a [ i ] , "id" ) -> s , id ) ) terms = get ( get ( relations -> a [ i ] , "rhs" ) , "terms" ) ;
    if ( ! terms ) die ( id ) ;
    Mat s = mat ( n , 0 ) ;
    for ( int i = 0 ; i < terms -> n ; i ++ ) {
        J * term = terms -> a [ i ] , * word = get ( term , "word" ) ;
        Mat a = copy ( local [ 0 ] ) ;
        for ( int w = 0 ; w < word -> n ; w ++ ) {
            char * name = word -> a [ w ] -> s ;
            Mat b ;
            if ( ! strcmp ( name , "H" ) ) b = h ;
            else if ( ! strcmp ( name , "H2" ) ) b = h2 ;
            else if ( ! strcmp ( name , "K" ) ) b = k ;
            else if ( ! strcmp ( name , "U" ) ) b = local [ 1 ] ;
            else die ( "braid word" ) ;
            Mat t = mm ( a , b ) ;
            mc ( & a ) ;
            a = t ;
        }
        Rat c ;
        init ( & c ) ;
        expr ( & c , get ( term , "coefficient" ) -> s ) ;
        addscaled ( s , a , & c ) ;
        clear ( & c ) ;
        mc ( & a ) ;
    }
    plus ( s , local [ 6 ] ) ;
    plus ( s , local [ 7 ] ) ;
    plus ( s , local [ 15 ] ) ;
    mc ( & h ) ;
    mc ( & h2 ) ;
    mc ( & k ) ;
    return s ;
}
static void term ( Mat r , Mat a , const char * s ) {
    Rat c ;
    init ( & c ) ;
    expr ( & c , s ) ;
    addscaled ( r , a , & c ) ;
    clear ( & c ) ;
}
/* Paper equation (8.3) times the polynomial-normalization scalar in Section 8.
   X=[x], Z=[x+2n], W=[x+3n], F=[6n]^2[n]/([3n]^2[2n]). */
static Mat construct ( Mat g [ 30 ] , J * recipes , J * ordinary ) {
    int n = g [ 0 ] . n ;
    Mat l [ 16 ] ;
    for ( int i = 0 ; i < 16 ; i ++ ) l [ i ] = mat ( n , 0 ) ;
    for ( int i = 0 ; i < recipes -> n ; i += 2 ) {
        int k = ji ( recipes -> a [ i ] ) ;
        J * words = recipes -> a [ i + 1 ] ;
        for ( int j = 0 ; j < words -> n ; j ++ ) {
            Mat a = mat ( n , 1 ) ;
            for ( int w = 0 ; w < words -> a [ j ] -> n ; w ++ ) {
                int idx = ji ( words -> a [ j ] -> a [ w ] ) ;
                if ( idx < 0 || idx >= 30 ) die ( "embedding index" ) ;
                Mat t = mm ( a , g [ idx ] ) ;
                mc ( & a ) ;
                a = t ;
            }
            plus ( l [ k ] , a ) ;
            mc ( & a ) ;
        }
    }
    Mat s = polynomial ( l , ordinary , "S_polynomial" ) , si = polynomial ( l , ordinary , "Sinv_polynomial" ) , r = mat ( n , 0 ) , identity = mat ( n , 1 ) ;
    term ( r , identity , "F*b11*Z*W" ) ;
    term ( r , s , "-F*p^-1*u^-1*X*Z*W/(q-q^-1)" ) ;
    term ( r , si , "F*p*u*X*Z*W/(q-q^-1)" ) ;
    term ( r , l [ 2 ] , "-F*b20*b30*b11*X/b60*b10*W" ) ;
    for ( int j = 9 ; j <= 12 ; j ++ ) term ( r , l [ j ] , "F*b20*b30*b11*X/b60*W" ) ;
    int bs [ ] = {
        6 , 7 , 5 , 8
    }
    ;
    for ( int j = 0 ; j < 4 ; j ++ ) term ( r , l [ bs [ j ] ] , "-F*b20*b30*b11*X/b60*W/b10" ) ;
    for ( int j = 13 ; j <= 14 ; j ++ ) term ( r , l [ j ] , "-F*b20*b30*b11*X/b60*(u+u^-1)" ) ;
    term ( r , l [ 1 ] , "F*b20*b30*b11*X/b60*(b60/b30*Z-W)/b10" ) ;
    term ( r , l [ 15 ] , "-F*b20*b30*b11*X/b60*(p^6*u+p^-6*u^-1+2*W/b10)" ) ;
    mc ( & s ) ;
    mc ( & si ) ;
    mc ( & identity ) ;
    for ( int i = 0 ; i < 16 ; i ++ ) mc ( & l [ i ] ) ;
    return r ;
}
/* Polynomial matrices are dense arrays, with zero factors skipped. */
typedef struct {
    int n ;
    fmpz_mpoly_struct * e ;
}
PM ;
static PM pm ( int n ) {
    PM a = {
        n , calloc ( n * n , sizeof ( fmpz_mpoly_struct ) )
    }
    ;
    for ( int i = 0 ; i < n * n ; i ++ ) fmpz_mpoly_init ( a . e + i , ctx ) ;
    return a ;
}
static PM pmul ( PM a , PM b ) {
    int n = a . n ;
    PM c = pm ( n ) ;
    fmpz_mpoly_t t ;
    fmpz_mpoly_init ( t , ctx ) ;
    for ( int i = 0 ; i < n ; i ++ ) for ( int k = 0 ; k < n ; k ++ ) if ( ! fmpz_mpoly_is_zero ( a . e + i * n + k , ctx ) ) for ( int j = 0 ; j < n ; j ++ ) if ( ! fmpz_mpoly_is_zero ( b . e + k * n + j , ctx ) ) {
        fmpz_mpoly_mul ( t , a . e + i * n + k , b . e + k * n + j , ctx ) ;
        fmpz_mpoly_add ( c . e + i * n + j , c . e + i * n + j , t , ctx ) ;
    }
    fmpz_mpoly_clear ( t , ctx ) ;
    return c ;
}
static PM subst ( PM a , int uv ) {
    PM b = pm ( a . n ) ;
    ulong e [ 4 ] ;
    for ( int i = 0 ; i < a . n * a . n ; i ++ ) for ( slong t = 0 ; t < a . e [ i ] . length ; t ++ ) {
        fmpz_mpoly_get_term_exp_ui ( e , a . e + i , t , ctx ) ;
        if ( e [ 3 ] ) die ( "unexpected v" ) ;
        e [ 3 ] = e [ 2 ] ;
        if ( ! uv ) e [ 2 ] = 0 ;
        fmpz_mpoly_set_coeff_fmpz_ui ( b . e + i , a . e [ i ] . coeffs + t , e , ctx ) ;
    }
    return b ;
}
static long terms ( PM a ) {
    long s = 0 ;
    for ( int i = 0 ; i < a . n * a . n ; i ++ ) s += a . e [ i ] . length ;
    return s ;
}
static void phase ( const char * name , double t ) {
    printf ( "{\"phase\":\"%s\",\"seconds\":%.6f}\n" , name , t ) ;
    fflush ( stdout ) ;
}
int main ( int argc , char * * argv ) {
    if ( argc != 2 ) die ( "usage: verifier representation_index (run from repository root)" ) ;
    int idx = atoi ( argv [ 1 ] ) ;
    if ( idx < 0 || idx > 10 ) die ( "index" ) ;
    double start = now ( ) ;
    fmpz_mpoly_ctx_init ( ctx , 4 , ORD_LEX ) ;
    flint_set_num_threads ( 1 ) ;
    for ( int i = 0 ; i < 4 ; i ++ ) {
        env [ ne ] . name = strdup ( vars [ i ] ) ;
        init ( & env [ ne ] . r ) ;
        fmpz_mpoly_gen ( env [ ne ] . r . n , i , ctx ) ;
        ne ++ ;
    }
    J * ordinary = readj ( "data/local_a2.json" ) ;
    defs = get ( ordinary , "coefficients" ) ;
    J * reg = readj ( "data/dilute_a3.json" ) , * emb = get ( readj ( "reports/paper_audit/local_embeddings.json" ) , "positions" ) ;
    char path [ 256 ] ;
    snprintf ( path , sizeof path , "data/dilute_representations/Dilute_%d.json" , idx ) ;
    J * doc = readj ( path ) ;
    int n = ji ( get ( doc , "dimension" ) ) ;
    bind ( "beta" , get ( get ( reg , "normalization_prescriptions" ) , "beta" ) -> s ) ;
    bind ( "F" , "b60^2*b10/(b30^2*b20)" ) ;
    bind ( "X" , "(u-u^-1)/(q-q^-1)" ) ;
    bind ( "Z" , "(p^2*u-p^-2*u^-1)/(q-q^-1)" ) ;
    bind ( "W" , "(p^3*u-p^-3*u^-1)/(q-q^-1)" ) ;
    bind ( "factor" , "F*(p*q*u-p^-1*q^-1*u^-1)/(q-q^-1)*(u*q^-1-u^-1*q)/(q-q^-1)*Z*W" ) ;
    Mat g [ 30 ] ;
    J * mats = get ( doc , "matrices" ) , * specs = get ( reg , "generators" ) ;
    if ( mats -> n != 30 || specs -> n != 30 ) die ( "generator count" ) ;
    for ( int k = 0 ; k < 30 ; k ++ ) {
        J * m = mats -> a [ k ] , * spec = specs -> a [ k ] ;
        if ( strcmp ( get ( m , "operator" ) -> s , get ( spec , "operator" ) -> s ) ) die ( "generator order" ) ;
        g [ k ] = mat ( n , 0 ) ;
        Rat scale ;
        init ( & scale ) ;
        expr ( & scale , get ( spec , "paper2_multiplier" ) -> s ) ;
        J * entries = get ( m , "entries" ) ;
        for ( int t = 0 ; t < entries -> n ; t ++ ) {
            J * a = entries -> a [ t ] ;
            int i = ji ( a -> a [ 0 ] ) , j = ji ( a -> a [ 1 ] ) ;
            if ( i < 0 || i >= n || j < 0 || j >= n ) die ( "entry index" ) ;
            expr ( g [ k ] . e + i * n + j , a -> a [ 2 ] -> s ) ;
            op ( g [ k ] . e + i * n + j , g [ k ] . e + i * n + j , & scale , '*' ) ;
        }
        clear ( & scale ) ;
    }
    phase ( "generators" , now ( ) - start ) ;
    Mat r [ 2 ] ;
    r [ 0 ] = construct ( g , get ( emb , "1" ) , ordinary ) ;
    phase ( "R1_constructed" , now ( ) - start ) ;
    r [ 1 ] = construct ( g , get ( emb , "2" ) , ordinary ) ;
    double constructed = now ( ) ;
    phase ( "construction" , constructed - start ) ;
    /* Independently compare with prior rational audit artifacts, never use them to build R. */
    snprintf ( path , sizeof path , "reports/paper_audit/spectral_%d.json" , idx ) ;
    J * positions = get ( readj ( path ) , "positions" ) ;
    for ( int pos = 0 ; pos < 2 ; pos ++ ) {
        Mat a = mat ( n , 0 ) ;
        J * es = get ( get ( positions , pos ? "2" : "1" ) , "entries" ) ;
        for ( int t = 0 ; t < es -> n ; t ++ ) {
            J * e = es -> a [ t ] ;
            expr ( a . e + ji ( e -> a [ 0 ] ) * n + ji ( e -> a [ 1 ] ) , e -> a [ 2 ] -> s ) ;
        }
        for ( int i = 0 ; i < n * n ; i ++ ) {
            Rat z ;
            init ( & z ) ;
            op ( & z , a . e + i , lookup ( "factor" ) , '*' ) ;
            op ( & z , r [ pos ] . e + i , & z , '-' ) ;
            if ( ! fmpz_mpoly_is_zero ( z . n , ctx ) ) {
                printf ( "{\"status\":\"FAIL\",\"check\":\"scalar_relationship\",\"position\":%d,\"row\":%d,\"column\":%d}\n" , pos + 1 , i / n , i % n ) ;
                fmpz_mpoly_print_pretty ( z . n , vars , ctx ) ;
                puts ( "" ) ;
                return 1 ;
            }
            clear ( & z ) ;
        }
        mc ( & a ) ;
    }
    phase ( "scalar_comparison" , now ( ) - constructed ) ;
    /* LCM of reduced denominators, same for both positions. Must be D(p,q)u^m. */
    double clearstart = now ( ) ;
    fmpz_mpoly_t den , gcd , t ;
    fmpz_mpoly_init ( den , ctx ) ;
    fmpz_mpoly_init ( gcd , ctx ) ;
    fmpz_mpoly_init ( t , ctx ) ;
    fmpz_mpoly_one ( den , ctx ) ;
    for ( int pos = 0 ; pos < 2 ; pos ++ ) for ( int i = 0 ; i < n * n ; i ++ ) {
        if ( ! fmpz_mpoly_gcd ( gcd , den , r [ pos ] . e [ i ] . d , ctx ) ) die ( "LCM gcd" ) ;
        fmpz_mpoly_divexact ( t , r [ pos ] . e [ i ] . d , gcd , ctx ) ;
        fmpz_mpoly_mul ( den , den , t , ctx ) ;
    }
    ulong e [ 4 ] ;
    fmpz_mpoly_get_term_exp_ui ( e , den , 0 , ctx ) ;
    ulong shift = e [ 2 ] ;
    for ( slong i = 0 ; i < den -> length ; i ++ ) {
        fmpz_mpoly_get_term_exp_ui ( e , den , i , ctx ) ;
        if ( e [ 2 ] != shift || e [ 3 ] ) die ( "non-monomial spectral denominator" ) ;
    }
    printf ( "{\"phase\":\"clearing_factor\",\"u_shift\":%lu,\"D_times_u_shift\":\"" , shift ) ;
    fmpz_mpoly_print_pretty ( den , vars , ctx ) ;
    puts ( "\"}" ) ;
    fflush ( stdout ) ;
    PM p [ 2 ] ;
    for ( int pos = 0 ; pos < 2 ; pos ++ ) {
        p [ pos ] = pm ( n ) ;
        for ( int i = 0 ; i < n * n ; i ++ ) {
            if ( ! fmpz_mpoly_divides ( t , den , r [ pos ] . e [ i ] . d , ctx ) ) die ( "denominator division" ) ;
            fmpz_mpoly_mul ( p [ pos ] . e + i , r [ pos ] . e [ i ] . n , t , ctx ) ;
        }
    }
    phase ( "denominator_clearing" , now ( ) - clearstart ) ;
    printf ( "{\"phase\":\"YBE_start\",\"R1_terms\":%ld,\"R2_terms\":%ld}\n" , terms ( p [ 0 ] ) , terms ( p [ 1 ] ) ) ;
    fflush ( stdout ) ;
    double y = now ( ) ;
    PM a = pmul ( p [ 0 ] , subst ( p [ 1 ] , 1 ) ) ;
    phase ( "left_pair" , now ( ) - y ) ;
    PM left = pmul ( a , subst ( p [ 0 ] , 0 ) ) ;
    phase ( "left_triple" , now ( ) - y ) ;
    PM b = pmul ( subst ( p [ 1 ] , 0 ) , subst ( p [ 0 ] , 1 ) ) ;
    phase ( "right_pair" , now ( ) - y ) ;
    PM right = pmul ( b , p [ 1 ] ) ;
    phase ( "right_triple" , now ( ) - y ) ;
    for ( int i = 0 ; i < n * n ; i ++ ) {
        fmpz_mpoly_sub ( t , left . e + i , right . e + i , ctx ) ;
        if ( ! fmpz_mpoly_is_zero ( t , ctx ) ) {
            printf ( "{\"status\":\"FAIL\",\"check\":\"YBE\",\"row\":%d,\"column\":%d}\n" , i / n , i % n ) ;
            fmpz_mpoly_print_pretty ( t , vars , ctx ) ;
            puts ( "" ) ;
            return 1 ;
        }
    }
    printf ( "{\"status\":\"PASS\",\"representation\":%d,\"dimension\":%d,\"construction_seconds\":%.6f,\"ybe_seconds\":%.6f,\"total_seconds\":%.6f,\"left_terms\":%ld,\"right_terms\":%ld,\"residual_nonzero_entries\":0,\"flint_header\":\"%s\"}\n" , idx , n , constructed - start , now ( ) - y , now ( ) - start , terms ( left ) , terms ( right ) , FLINT_VERSION ) ;
    return 0 ;
}
