#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <time.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>
static double now ( void ) {
    struct timespec t ;
    clock_gettime ( CLOCK_MONOTONIC , & t ) ;
    return t . tv_sec + t . tv_nsec / 1e9 ;
}
int main ( int argc , char * * argv ) {
    const char * outdir = argc > 1 ? argv [ 1 ] : "benchmarks/flint_ybe" ;
    if ( mkdir ( outdir , 0755 ) != 0 && errno != EEXIST ) {
        perror ( outdir ) ;
        return 2 ;
    }
    char resultpath [ 1024 ] , reportpath [ 1024 ] ;
    snprintf ( resultpath , sizeof resultpath , "%s/results.json" , outdir ) ;
    snprintf ( reportpath , sizeof reportpath , "%s/results.md" , outdir ) ;
    int ids [ ] = {
        5 , 6 , 7 , 9 , 10 , 8 , 0 , 3 , 4 , 2 , 1
    }
    , dims [ ] = {
        1 , 1 , 1 , 2 , 2 , 3 , 5 , 6 , 6 , 7 , 11
    }
    ;
    const char * names [ ] = {
        "X3" , "Y3" , "Y3_star" , "C" , "C_star" , "A" , "I" , "Y2" , "Y2_star" , "X2" , "L"
    }
    ;
    FILE * out = fopen ( resultpath , "wx" ) , * md = fopen ( reportpath , "wx" ) ;
    if ( ! out || ! md ) {
        perror ( "Refusing to overwrite results" ) ;
        return 2 ;
    }
    fprintf ( out , "{\"per_representation_limit_seconds\":60,\"batch_limit_seconds\":300,\"results\":[\n" ) ;
    fprintf ( md , "| Representation | Dimension | Status | Wall seconds | Peak RSS MiB | Last phase |\n|---|---:|---|---:|---:|---|\n" ) ;
    double batch = now ( ) ;
    int allpass = 1 ;
    for ( int k = 0 ; k < 11 ; k ++ ) {
        double start = now ( ) , available = 300 - ( start - batch ) , limit = available < 60 ? available : 60 ;
        char log [ 1024 ] , arg [ 16 ] ;
        snprintf ( log , sizeof log , "%s/rep_%d.jsonl" , outdir , ids [ k ] ) ;
        snprintf ( arg , sizeof arg , "%d" , ids [ k ] ) ;
        const char * status = "NOT ATTEMPTED" ;
        struct rusage usage = {
            0
        }
        ;
        int code = - 1 , expired = 0 ;
        double elapsed = 0 ;
        if ( limit > 0 ) {
            pid_t child = fork ( ) ;
            if ( child == 0 ) {
                setpgid ( 0 , 0 ) ;
                int fd = open ( log , O_WRONLY | O_CREAT | O_EXCL , 0644 ) ;
                if ( fd < 0 ) _exit ( 2 ) ;
                dup2 ( fd , 1 ) ;
                dup2 ( fd , 2 ) ;
                close ( fd ) ;
                execl ( "benchmarks/flint_ybe/verifier" , "verifier" , arg , ( char * ) NULL ) ;
                _exit ( 2 ) ;
            }
            if ( child < 0 ) {
                perror ( "fork" ) ;
                return 2 ;
            }
            setpgid ( child , child ) ;
            int w ;
            while ( wait4 ( child , & w , WNOHANG , & usage ) == 0 ) {
                if ( now ( ) - start >= limit ) {
                    expired = 1 ;
                    kill ( - child , SIGKILL ) ;
                    wait4 ( child , & w , 0 , & usage ) ;
                    break ;
                }
                struct timespec pause = {
                    0 , 5000000
                }
                ;
                nanosleep ( & pause , NULL ) ;
            }
            elapsed = now ( ) - start ;
            code = WIFEXITED ( w ) ? WEXITSTATUS ( w ) : - 1 ;
            status = expired ? "TIMEOUT" : code == 0 ? "PASS" : code == 1 ? "FAIL" : "ERROR" ;
        }
        char phase [ 80 ] = "none" , line [ 16384 ] ;
        FILE * f = fopen ( log , "r" ) ;
        if ( f ) {
            while ( fgets ( line , sizeof line , f ) ) {
                char * s = strstr ( line , "\"phase\":\"" ) ;
                if ( s ) {
                    s += 9 ;
                    char * e = strchr ( s , '"' ) ;
                    if ( e && e - s < 79 ) {
                        memcpy ( phase , s , e - s ) ;
                        phase [ e - s ] = 0 ;
                    }
                }
            }
            fclose ( f ) ;
        }
        if ( strcmp ( status , "PASS" ) ) allpass = 0 ;
        fprintf ( out , "%s{\"representation\":\"%s\",\"index\":%d,\"dimension\":%d,\"status\":\"%s\",\"wall_seconds\":%.6f,\"peak_rss_kib\":%ld,\"last_phase\":\"%s\",\"exit_code\":%d,\"effective_limit_seconds\":%.6f}" , k ? ",\n" : "" , names [ k ] , ids [ k ] , dims [ k ] , status , elapsed , usage . ru_maxrss , phase , code , limit > 0 ? limit : 0 ) ;
        fprintf ( md , "| %s | %d | %s | %.3f | %.2f | %s |\n" , names [ k ] , dims [ k ] , status , elapsed , usage . ru_maxrss / 1024.0 , phase ) ;
        fflush ( out ) ;
        fflush ( md ) ;
        printf ( "%s %s %.3fs %.2fMiB (%s)\n" , names [ k ] , status , elapsed , usage . ru_maxrss / 1024.0 , phase ) ;
        fflush ( stdout ) ;
    }
    fprintf ( out , "\n],\"batch_wall_seconds\":%.6f,\"all_eleven_pass\":%s}\n" , now ( ) - batch , allpass ? "true" : "false" ) ;
    fclose ( out ) ;
    fclose ( md ) ;
    return 0 ;
}
