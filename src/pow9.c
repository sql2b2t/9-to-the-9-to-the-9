/*
 * Compute 9^(9^9) exactly and write its decimal representation.
 *
 * GMP stores the result as a ~154 MiB binary integer; converting it to decimal
 * is the expensive part of the run. Use tools/verify.py to check the output.
 */
#include <gmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define EXPONENT 387420489UL /* 9^9 */

static double now(void)
{
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

int main(int argc, char **argv)
{
    const char *path = argc > 1 ? argv[1] : "9_9_9.txt";
    mpz_t n;
    char *s;
    size_t ndigits, len;
    FILE *f;
    double t0, t1, t2, t3;

    t0 = now();

    mpz_init(n);
    mpz_ui_pow_ui(n, 9, EXPONENT);
    t1 = now();

    ndigits = mpz_sizeinbase(n, 10);
    s = mpz_get_str(NULL, 10, n);
    if (s == NULL) {
        fputs("mpz_get_str failed\n", stderr);
        mpz_clear(n);
        return EXIT_FAILURE;
    }
    t2 = now();

    len = strlen(s);
    if (len != ndigits) {
        fprintf(stderr, "length mismatch: strlen=%zu sizeinbase=%zu\n",
                len, ndigits);
        free(s);
        mpz_clear(n);
        return EXIT_FAILURE;
    }

    f = fopen(path, "w");
    if (f == NULL) {
        perror(path);
        free(s);
        mpz_clear(n);
        return EXIT_FAILURE;
    }
    if (fwrite(s, 1, len, f) != len || fputc('\n', f) == EOF || fclose(f) != 0) {
        perror(path);
        free(s);
        mpz_clear(n);
        return EXIT_FAILURE;
    }
    t3 = now();

    printf("digits=%zu\n", ndigits);
    printf("first30=%.30s\n", s);
    printf("last30=%s\n", s + len - 30);
    printf("pow=%.3fs tostr=%.3fs write=%.3fs total=%.3fs\n",
           t1 - t0, t2 - t1, t3 - t2, t3 - t0);

    free(s);
    mpz_clear(n);
    return EXIT_SUCCESS;
}
