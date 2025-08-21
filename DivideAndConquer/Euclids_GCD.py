# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 6
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ EUCLID'S GCD ------

def gcd_euclid(m, n):
    # gcd (m, n) = gcd (n, m mod n)
    # gcd(64, 24) = gcd(24, 12) = gcd(12, 0) = 12
    while n != 0:
        r = m % n
        m = n
        n = r
    return m

print(gcd_euclid(60, 24))
