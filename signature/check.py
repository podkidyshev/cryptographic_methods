import os
import sys
import zlib
from signing import read_4


def main():
    assert len(sys.argv) == 2, 'Передайте название файла'
    with open(os.path.abspath(sys.argv[1]), 'rb') as f:
        p = read_4(f)
        q = read_4(f)
        y = read_4(f)
        a = read_4(f)
        m = read_4(f)
        r = read_4(f)
        s = read_4(f)
        content_obj = f.read()
        # content = content_obj.decode(encoding='utf-8')

    assert 0 < r < p, 'Подпись неверна'
    assert 0 < s < q, 'Подпись неверна'
    assert m == zlib.crc32(content_obj) // 16, 'Нарушена целостность'
    assert pow(a, m, p) == (pow(y, r, p) * pow(r, s, p)) % p, 'Подпись неверна'
    print('Подпись верна')

    content = content_obj.decode(encoding='utf-8')
    print(content)


if __name__ == '__main__':
    main()
