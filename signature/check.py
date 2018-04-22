import os
import sys


def main():
    assert len(sys.argv) == 2, 'Передайте название файла'
    with open(os.path.abspath(sys.argv[1]), 'r') as f:
        p = int(f.readline())
        q = int(f.readline())
        y = int(f.readline())
        a = int(f.readline())
        m = int(f.readline())
        r = int(f.readline())
        s = int(f.readline())

    assert 0 < r < p, 'Подпись неверна'
    assert 0 < s < q, 'Подпись неверна'
    assert pow(a, m, p) == (pow(y, r, p) * pow(r, s, p)) % p, 'Подпись неверна'
    print('Подпись верна')


if __name__ == '__main__':
    main()
