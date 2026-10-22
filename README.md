# 9^9^9

Exact decimal value of the power tower

```
9^(9^9) = 9^387420489
```

Exponentiation is right-associative, so this is `9^(9^9)`, not `(9^9)^9`.

## Artifact

| Property | Value |
| --- | --- |
| Decimal digits | 369,693,100 |
| File size | 369,693,101 bytes (digits plus one trailing newline) |
| First 30 digits | `428124773175747048036987115930` |
| Last 40 digits | `6190174923494324178799359681422627177289` |
| SHA-256 | `e2b8d7a6fc5ef75a16e63a0da4f5ad84fa701ec15b6d3585afc7691ef58fcb42` |

The value is about `4.2812e369693099`.

GitHub limits tracked files to 100 MB, so the 353 MiB text file is not stored
in the repository. It is attached to the release as the asset `9_9_9.txt`.

## Regenerating

Requirements: a C compiler, GMP (headers and library).

```sh
make
./pow9 9_9_9.txt
```

The program computes the value with `mpz_ui_pow_ui` and writes the decimal
representation followed by a newline. On a modern x86-64 machine the run takes
about 92 seconds, of which ~87 seconds are spent converting the 154 MiB binary
integer to decimal.

## Verifying

```sh
python3 tools/verify.py 9_9_9.txt
```

The verifier checks the file structure, the digit count, the leading and
trailing digits, the SHA-256 checksum, and the value of the entire decimal
string modulo several moduli against `pow(9, 9**9, m)`.

## Repository layout

```
src/pow9.c        generator (GMP)
tools/verify.py   independent verifier
Makefile          build rules
```
