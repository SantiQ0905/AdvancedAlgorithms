# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 6
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ STEIN'S GCD ------

def gcd_stein(a, b):

    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a

    # Remove common powers of two
    shift = 0
    while ((a | b) & 1) == 0:  # both even
        a >>= 1
        b >>= 1
        shift += 1

    # Make a odd
    while (a & 1) == 0:
        a >>= 1

    # Main loop: keep b odd, ensure a <= b, subtract
    while b != 0:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b -= a
    return a << shift  # restore common power of two


if __name__ == "__main__":
    # Tiny sanity check / demo
    tests = [(0, 0), (0, 18), (18, 0), (54, 24), (-54, 24), (270, 192)]
    for x, y in tests:
        print(f"gcd_stein({x}, {y}) = {gcd_stein(x, y)}")
