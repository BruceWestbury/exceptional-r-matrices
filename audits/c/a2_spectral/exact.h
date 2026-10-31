/* Adapted arithmetic/JSON/scalar infrastructure from benchmarks/flint_ybe/verifier.c. No spectral calculation copied. */
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
    "p" , "q" , "u"
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
