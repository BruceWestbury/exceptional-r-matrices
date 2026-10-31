/* Reused JSON-only reader from benchmarks/flint_ybe; no spectral arithmetic. */
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
