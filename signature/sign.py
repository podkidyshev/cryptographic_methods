import os
import sys
import signing


def main():
    assert len(sys.argv) == 2, 'Передайте название файла'
    with open(os.path.abspath(sys.argv[1])) as f:
        content = f.read()

    content_bytes = content.encode('utf-8')
    sign = signing.sign(content_bytes)

    with open(os.path.abspath('.\\a.signed'), 'w') as f:
        for param in sign:
            f.write('{}\n'.format(param))
        f.write(content)


if __name__ == '__main__':
    main()
