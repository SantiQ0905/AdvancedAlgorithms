# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ----- CLASS ACTIVITY 2: DECREASE AND CONQUER -----


def pow_dec_rec_safe(a, n):
    # Reject non-integer exponents without raising
    if not isinstance(n, int):
        return None, "Exponent must be an integer"

    # Handle negative exponents without raising
    if n < 0:
        if a == 0:
            return None, "Undefined: 0 to a negative power"
        # a^(-n) = (1/a)^n
        return pow_dec_rec_safe(1.0 / a, -n)

    # Base cases
    if n == 0:
        return 1, None
    if n == 1:
        return a, None

    # Decrease step: n -> n-1
    sub, err = pow_dec_rec_safe(a, n - 1)
    if err is not None:
        return None, err
    return a * sub, None


def pow_dec_iter_safe(a, n):
    """
    Iterative decrease-and-conquer power (preferred in Python to avoid recursion limits).
    Returns: (value, error)
    """
    if not isinstance(n, int):
        return None, "Exponent must be an integer"

    if n < 0:
        if a == 0:
            return None, "Undefined: 0 to a negative power"
        a, n = 1.0 / a, -n

    result = 1
    for _ in range(n):
        result *= a
    return result, None


# --- Tiny self-checks without `assert` ---
def _almost_equal(x, y, eps=1e-12):
    # Works for int/float; avoids exceptions for None
    return (x == y) if (isinstance(x, int) and isinstance(y, int)) else (abs(x - y) < eps)

if __name__ == "__main__":
    tests = [
        (2, 10), (2, 1), (2, 0), (2, -3),
        (-3, 5), (-3, 2), (0, 0), (0, 5),
        (0, -1), (2.5, 3), (2.5, -2), (2, 3.0)  # last one should error (non-int exponent)
    ]
    for a, n in tests:
        val_i, err_i = pow_dec_iter_safe(a, n)
        val_r, err_r = pow_dec_rec_safe(a, n)

        # Print outcomes instead of asserting
        if err_i or err_r:
            print(f"{a}^{n} -> error (iter='{err_i}', rec='{err_r}')")
        else:
            # Compare to built-in when safe (avoid 0**negative)
            if not (a == 0 and n < 0):
                builtin = a ** n
                ok_i = _almost_equal(val_i, builtin)
                ok_r = _almost_equal(val_r, builtin)
                print(f"{a}^{n} -> iter={val_i} (ok={ok_i}), rec={val_r} (ok={ok_r})")
            else:
                print(f"{a}^{n} -> undefined (by math), got iter={val_i}, rec={val_r}")
