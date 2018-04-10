import os
import sys
import signing


def main():
    assert len(sys.argv) == 2, 'Передайте название файла'
    with open(os.path.abspath(sys.argv[1]), 'rb') as f:
        size = int.from_bytes(f.read(signing.DEFAULT_BYTES_LEN), byteorder='big')
        content_bytes = f.read(size)
        sign = f.read()

    if sign != signing.signature(content_bytes):
        print('Неверная подпись!')
    else:
        print('Подпись верная')
        print(content_bytes.decode('utf-8'))


if __name__ == '__main__':
    main()
