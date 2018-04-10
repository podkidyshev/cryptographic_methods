import os
import sys
import signing


def main():
    assert len(sys.argv) == 2, 'Передайте название файла'
    with open(os.path.abspath(sys.argv[1])) as f:
        content = f.read()

    content_bytes = content.encode('utf-8')
    size = signing.int_to_bytes(len(content_bytes))
    sign = signing.signature(content_bytes)

    with open(os.path.abspath('.\\a.signed'), 'wb') as f:
        f.write(size)
        f.write(content_bytes)
        f.write(sign)


if __name__ == '__main__':
    main()
