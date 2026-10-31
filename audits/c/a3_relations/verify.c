#define _POSIX_C_SOURCE 200809L
#include <flint/fmpq_mpoly.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <time.h>

static fmpq_mpoly_ctx_t ring;
static const char *variables[] = {"p", "q"};
static void die(const char *message) {
    fprintf(stderr, "ERROR: %s\n", message);
    exit(2);
}
#include "json_reader.h"

static double seconds(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}
static long memory(void) {
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    return r.ru_maxrss;
}
/* Rational functions represented by reduced Q[p,q] numerator/denominator.
   Polynomial division is always checked, never an assumed cancellation. */
typedef struct { fmpq_mpoly_t numerator, denominator; } Scalar;
static void scalar_init(Scalar *a) {
    fmpq_mpoly_init(a->numerator, ring);
    fmpq_mpoly_init(a->denominator, ring);
    fmpq_mpoly_one(a->denominator, ring);
}
static void scalar_clear(Scalar *a) {
    fmpq_mpoly_clear(a->numerator, ring);
    fmpq_mpoly_clear(a->denominator, ring);
}
static void scalar_copy(Scalar *a, const Scalar *b) {
    fmpq_mpoly_set(a->numerator, b->numerator, ring);
    fmpq_mpoly_set(a->denominator, b->denominator, ring);
}
static void scalar_integer(Scalar *a, long n) {
    fmpq_mpoly_set_si(a->numerator, n, ring);
    fmpq_mpoly_one(a->denominator, ring);
}
static int nonzero(const Scalar *a) {
    return !fmpq_mpoly_is_zero(a->numerator, ring);
}
static void normalize(Scalar *a) {
    if (fmpq_mpoly_is_zero(a->denominator, ring)) die("division by zero");
    if (!nonzero(a)) {
        fmpq_mpoly_one(a->denominator, ring);
        return;
    }
    fmpq_mpoly_t gcd, n, d;
    fmpq_mpoly_init(gcd, ring); fmpq_mpoly_init(n, ring); fmpq_mpoly_init(d, ring);
    if (!fmpq_mpoly_gcd_cofactors(gcd, n, d, a->numerator, a->denominator, ring))
        die("exact gcd cofactors failed");
    fmpq_mpoly_set(a->numerator, n, ring);
    fmpq_mpoly_set(a->denominator, d, ring);
    fmpq_mpoly_clear(gcd, ring); fmpq_mpoly_clear(n, ring); fmpq_mpoly_clear(d, ring);
}
static void arithmetic(Scalar *out, const Scalar *a, const Scalar *b, char operation) {
    Scalar t; scalar_init(&t);
    if (operation == '+' || operation == '-') {
        fmpq_mpoly_t second; fmpq_mpoly_init(second, ring);
        fmpq_mpoly_mul(t.numerator, a->numerator, b->denominator, ring);
        fmpq_mpoly_mul(second, b->numerator, a->denominator, ring);
        if (operation == '+') fmpq_mpoly_add(t.numerator, t.numerator, second, ring);
        else fmpq_mpoly_sub(t.numerator, t.numerator, second, ring);
        fmpq_mpoly_mul(t.denominator, a->denominator, b->denominator, ring);
        fmpq_mpoly_clear(second, ring);
    } else {
        fmpq_mpoly_mul(t.numerator, a->numerator,
                      operation == '*' ? b->numerator : b->denominator, ring);
        fmpq_mpoly_mul(t.denominator, a->denominator,
                      operation == '*' ? b->denominator : b->numerator, ring);
    }
    normalize(&t); scalar_copy(out, &t); scalar_clear(&t);
}
static void exponentiate(Scalar *a, long exponent) {
    Scalar t; scalar_init(&t);
    if (!fmpq_mpoly_pow_ui(t.numerator, exponent < 0 ? a->denominator : a->numerator,
                          labs(exponent), ring) ||
        !fmpq_mpoly_pow_ui(t.denominator, exponent < 0 ? a->numerator : a->denominator,
                          labs(exponent), ring)) die("power failed");
    normalize(&t); scalar_copy(a, &t); scalar_clear(&t);
}
/* Recursive descent for the repository's restricted scalar grammar. */
static J *definitions;
typedef struct { char *name; int ready; Scalar value; } Coefficient;
static Coefficient coefficients[256];
static int coefficient_count;
static void parse(Scalar *, const char *);
static Scalar *coefficient(const char *name) {
    for (int i = 0; i < coefficient_count; ++i) {
        if (strcmp(name, coefficients[i].name)) continue;
        if (!coefficients[i].ready) die("cyclic coefficient definition");
        return &coefficients[i].value;
    }
    if (coefficient_count == 256) die("coefficient capacity");
    Coefficient *c = coefficients + coefficient_count++;
    c->name = strdup(name); scalar_init(&c->value);
    parse(&c->value, get(get(definitions, name), "expression")->s);
    c->ready = 1;
    return &c->value;
}
static void expression(Scalar *, const char **);
static void primary(Scalar *a, const char **text) {
    ws(text);
    if (**text == '-' || **text == '+') {
        char sign = *(*text)++;
        primary(a, text);
        if (sign == '-') fmpq_mpoly_neg(a->numerator, a->numerator, ring);
        return;
    }
    if (**text == '(') {
        ++*text; expression(a, text); ws(text);
        if (*(*text)++ != ')') die("expected closing parenthesis");
    } else if (isdigit((unsigned char)**text)) {
        const char *start = *text;
        while (isdigit((unsigned char)**text)) ++*text;
        char *literal = strndup(start, *text - start);
        if (fmpq_mpoly_set_str_pretty(a->numerator, literal, variables, ring))
            die("integer literal");
        fmpq_mpoly_one(a->denominator, ring); free(literal);
    } else if (isalpha((unsigned char)**text) || **text == '_') {
        const char *start = *text;
        while (isalnum((unsigned char)**text) || **text == '_') ++*text;
        char *name = strndup(start, *text - start);
        scalar_copy(a, coefficient(name)); free(name);
    } else die("unexpected scalar token");
    ws(text);
    if (**text == '^') {
        ++*text; ws(text);
        int parentheses = **text == '(';
        if (parentheses) ++*text;
        char *end; long exponent = strtol(*text, &end, 10);
        if (end == *text || exponent < -10000 || exponent > 10000) die("invalid exponent");
        *text = end; ws(text);
        if (parentheses && *(*text)++ != ')') die("exponent parenthesis");
        exponentiate(a, exponent);
    }
}
static void product(Scalar *a, const char **text) {
    primary(a, text); ws(text);
    while (**text == '*' || **text == '/') {
        char operation = *(*text)++; Scalar b; scalar_init(&b);
        primary(&b, text); arithmetic(a, a, &b, operation); scalar_clear(&b); ws(text);
    }
}
static void expression(Scalar *a, const char **text) {
    product(a, text); ws(text);
    while (**text == '+' || **text == '-') {
        char operation = *(*text)++; Scalar b; scalar_init(&b);
        product(&b, text); arithmetic(a, a, &b, operation); scalar_clear(&b); ws(text);
    }
}
static void parse(Scalar *a, const char *text) {
    expression(a, &text); ws(&text);
    if (*text) die("trailing scalar text");
}

typedef struct { int size; Scalar *entry; } Matrix;
static Matrix matrix(int n, int identity) {
    Matrix m = {n, calloc(n*n, sizeof(Scalar))};
    for (int i = 0; i < n*n; ++i) {
        scalar_init(m.entry+i);
        if (identity && i/n == i%n) scalar_integer(m.entry+i, 1);
    }
    return m;
}
static void release(Matrix m) {
    for (int i = 0; i < m.size*m.size; ++i) scalar_clear(m.entry+i);
    free(m.entry);
}
static Matrix multiply(Matrix a, Matrix b) {
    int n = a.size; Matrix out = matrix(n, 0); Scalar t; scalar_init(&t);
    for (int i = 0; i < n; ++i) for (int k = 0; k < n; ++k) {
        if (!nonzero(a.entry+i*n+k)) continue;
        for (int j = 0; j < n; ++j) {
            if (!nonzero(b.entry+k*n+j)) continue;
            arithmetic(&t, a.entry+i*n+k, b.entry+k*n+j, '*');
            arithmetic(out.entry+i*n+j, out.entry+i*n+j, &t, '+');
        }
    }
    scalar_clear(&t); return out;
}
/* Cache ordered word prefixes, never commute or reverse them. */
static Matrix generators[16];
static char *generator_names[16];
static int generator_count;
typedef struct { char *key; Matrix value; } Word;
static Word words[2048]; static int word_count;
static Matrix word(J *names) {
    char key[1024] = "";
    Matrix current = words[0].value;
    for (int i = 0; i < names->n; ++i) {
        const char *name = names->a[i]->s;
        if (strlen(key)+strlen(name)+2 >= sizeof key) die("word too long");
        strcat(key, name); strcat(key, ",");
        int cached = -1;
        for (int j = 0; j < word_count; ++j) if (!strcmp(key, words[j].key)) { cached=j; break; }
        if (cached >= 0) { current = words[cached].value; continue; }
        int g = -1;
        for (int j = 0; j < generator_count; ++j) if (!strcmp(name, generator_names[j])) g=j;
        if (g < 0 || word_count == 2048) die("unknown generator or word capacity");
        current = multiply(current, generators[g]);
        words[word_count++] = (Word){strdup(key), current};
    }
    return current;
}
static void accumulate(Matrix residual, J *side, int sign) {
    J *terms = get(side, "terms"); Scalar c, t; scalar_init(&c); scalar_init(&t);
    for (int i = 0; i < terms->n; ++i) {
        J *term = terms->a[i];
        parse(&c, get(term, "coefficient")->s);
        if (sign < 0) fmpq_mpoly_neg(c.numerator, c.numerator, ring);
        Matrix m = word(get(term, "word"));
        for (int j = 0; j < m.size*m.size; ++j) {
            if (!nonzero(m.entry+j)) continue;
            arithmetic(&t, &c, m.entry+j, '*');
            arithmetic(residual.entry+j, residual.entry+j, &t, '+');
        }
    }
    scalar_clear(&c); scalar_clear(&t);
}
static int applies(J *relation, const char *representation) {
    J *names = get(relation, "applicable_representations");
    for (int i = 0; i < names->n; ++i) if (!strcmp(names->a[i]->s, representation)) return 1;
    return 0;
}
static void sources(J *relation) {
    J *source = get(relation, "current_manuscript_source");
    printf("\"source\":[");
    for (int i = 0; i < source->n; ++i) printf("%s\"%s\"", i?",":"", source->a[i]->s);
    printf("]");
}
int main(int argc, char **argv) {
    if (argc != 2) die("run from repository root: verify REPRESENTATION");
    double start = seconds();
    flint_set_num_threads(1); fmpq_mpoly_ctx_init(ring, 2, ORD_DEGREVLEX);
    J *manifest = readj("audits/c/a3_relations/manifest.json");
    definitions = get(manifest, "coefficients");
    for (int i = 0; i < 2; ++i) {
        Coefficient *c = coefficients+coefficient_count++;
        c->name = strdup(variables[i]); c->ready=1; scalar_init(&c->value);
        fmpq_mpoly_gen(c->value.numerator, i, ring);
    }
    J *representations = get(manifest, "representations"), *spec = NULL;
    for (int i = 0; i < representations->n; ++i)
        if (!strcmp(get(representations->a[i], "id")->s, argv[1])) spec=representations->a[i];
    if (!spec) die("unregistered representation");
    J *document = readj(get(spec, "path")->s);
    int n = ji(get(document, "dimension"));
    J *mats = get(document, "matrices"); generator_count = mats->n;
    if (generator_count != 10 || n != ji(get(spec, "dimension"))) die("matrix inventory");
    for (int i = 0; i < generator_count; ++i) {
        J *m = mats->a[i]; generator_names[i] = get(m, "operator")->s;
        generators[i] = matrix(n, 0); J *entries = get(m, "entries");
        if (ji(get(m,"rows")) != n || ji(get(m,"cols")) != n) die("matrix dimensions");
        for (int j = 0; j < entries->n; ++j) {
            J *e = entries->a[j]; int row=ji(e->a[0]), col=ji(e->a[1]);
            if (row<0 || col<0 || row>=n || col>=n) die("entry bounds");
            parse(generators[i].entry+row*n+col, e->a[2]->s);
        }
    }
    words[word_count++] = (Word){strdup(""), matrix(n, 1)};
    printf("{\"phase\":\"loaded\",\"representation\":\"%s\",\"seconds\":%.6f}\n", argv[1], seconds()-start);
    J *relations = get(manifest, "relations"); int failed=0, passed=0, skipped=0;
    for (int r = 0; r < relations->n; ++r) {
        J *relation = relations->a[r]; const char *id = get(relation, "id")->s;
        double t = seconds();
        if (!applies(relation, argv[1])) {
            printf("{\"representation\":\"%s\",\"id\":\"%s\",\"status\":\"NOT APPLICABLE\",\"residuals\":null,\"seconds\":0,\"peak_rss_kib\":%ld,", argv[1], id, memory());
            sources(relation); puts("}"); ++skipped; continue;
        }
        printf("{\"phase\":\"relation_started\",\"id\":\"%s\"}\n", id); fflush(stdout);
        Matrix residual = matrix(n, 0);
        accumulate(residual, get(relation,"lhs"), 1); accumulate(residual, get(relation,"rhs"), -1);
        int count=0; for (int i=0; i<n*n; ++i) if (nonzero(residual.entry+i)) ++count;
        printf("{\"representation\":\"%s\",\"id\":\"%s\",\"status\":\"%s\",\"seconds\":%.6f,\"peak_rss_kib\":%ld,\"checked_entries\":%d,",argv[1],id,count?"FAIL":"PASS",seconds()-t,memory(),n*n);
        sources(relation); printf(",\"residuals\":["); int emitted=0;
        for (int i=0; i<n*n; ++i) if (nonzero(residual.entry+i)) {
            printf("%s{\"row\":%d,\"column\":%d,\"numerator\":\"",emitted++?",":"",i/n,i%n);
            fmpq_mpoly_print_pretty(residual.entry[i].numerator,variables,ring);
            printf("\",\"denominator\":\"");
            fmpq_mpoly_print_pretty(residual.entry[i].denominator,variables,ring);
            printf("\"}");
        }
        puts("]}"); fflush(stdout); release(residual);
        if (count) ++failed; else ++passed;
    }
    printf("{\"phase\":\"complete\",\"representation\":\"%s\",\"status\":\"%s\",\"passed\":%d,\"failed\":%d,\"not_applicable\":%d,\"seconds\":%.6f,\"peak_rss_kib\":%ld,\"cached_words\":%d}\n",argv[1],failed?"FAIL":"PASS",passed,failed,skipped,seconds()-start,memory(),word_count);
    return failed?1:0;
}
