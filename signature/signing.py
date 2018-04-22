import zlib
import random

from sympy.ntheory import factorint

big_primes = [
    32416188349,
    32416184123,
    21201258823,
    18782080909,
    18782083511,
]


def sign(obj):
    m = zlib.crc32(obj) // 16
    p, q, a, x, y = generate_key()

    assert 0 < m < q, 'Не получаица'

    k = random.randint(0, q - 1)
    r = pow(a, k, p)
    s = (inverse(k, q) * (m - r * x)) % q
    k = -1  # уничтожение k

    return [p, q, y, a, m, r, s]


def generate_key():
    p = random.choice(big_primes)
    q = list(sorted(factorint(p - 1)))[-1]

    a = q - 1
    while pow(a, q, p) != 1:
        a -= 1

    x = random.randint(1, (p - 1) // 2)
    y = pow(a, x, p)

    with open('key.txt', 'w') as f:
        f.write('{}\n{}\n{}\n{}\n{}'.format(p, q, a, x, y))

    return p, q, a, x, y


def inverse(k, q):
    res = pow(k, q - 2, q)
    if (k * res) % q != 1:
        raise ArithmeticError('lol')
    return res
