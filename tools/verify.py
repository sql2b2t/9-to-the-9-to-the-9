#!/usr/bin/env python3
"""Verify the decimal expansion of 9^(9^9).

Checks performed:
  * file contains only digits and exactly one trailing newline
  * digit count matches 369,693,100
  * leading 30 and trailing 40 digits match known values
  * SHA-256 matches the published checksum
  * the whole decimal string, reduced modulo several moduli, equals
    pow(9, 9**9, m)

Usage: verify.py PATH
"""

import hashlib
import sys

EXPECTED_DIGITS = 369_693_100
EXPECTED_SHA256 = "e2b8d7a6fc5ef75a16e63a0da4f5ad84fa701ec15b6d3585afc7691ef58fcb42"
EXPECTED_PREFIX = b"428124773175747048036987115930"
EXPECTED_SUFFIX = b"6190174923494324178799359681422627177289"
EXPONENT = 9**9  # 387,420,489
MODULI = {
    "10^30": 10**30,
    "2^89-1": 2**89 - 1,
    "998244353": 998_244_353,
    "10^18+9": 10**18 + 9,
}
CHUNK = 8192


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("usage: verify.py PATH")

    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    if not data.endswith(b"\n") or data.count(b"\n") != 1:
        fail("expected exactly one trailing newline")
    digits = data[:-1]

    if len(digits) != EXPECTED_DIGITS:
        fail(f"digit count is {len(digits)}, expected {EXPECTED_DIGITS}")
    if not digits.isdigit():
        fail("file contains non-digit characters")

    if not digits.startswith(EXPECTED_PREFIX):
        fail("leading digits do not match")
    if not digits.endswith(EXPECTED_SUFFIX):
        fail("trailing digits do not match")

    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail(f"SHA-256 is {digest}, expected {EXPECTED_SHA256}")

    print(f"structure OK: {len(digits)} digits, SHA-256 OK")
    print(f"prefix OK: {EXPECTED_PREFIX.decode()}")
    print(f"suffix OK: {EXPECTED_SUFFIX.decode()}")

    ok = True
    for name, m in MODULI.items():
        value = 0
        for i in range(0, len(digits), CHUNK):
            chunk = digits[i : i + CHUNK]
            value = (value * pow(10, len(chunk), m) + int(chunk)) % m
        expected = pow(9, EXPONENT, m)
        status = "OK" if value == expected else "MISMATCH"
        if value != expected:
            ok = False
        print(f"mod {name}: {value} vs {expected} [{status}]")

    if not ok:
        fail("modular checks failed")
    print("all checks passed")


if __name__ == "__main__":
    main()
