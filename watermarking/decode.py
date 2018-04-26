import sys
from PIL import Image


def main():
    assert len(sys.argv) == 2, 'Передайте имя подписанного файла'

    im = Image.open(sys.argv[1])

    cbits = []
    mark = bytearray()

    for (x, y) in iter_im(im):
        handle_mark(cbits, mark, im.getpixel((x, y))[0] % 2)

    mark_len = int.from_bytes(mark[:4], byteorder='big')
    with open('unpacked.bin', 'wb') as f:
        f.write(mark[4:mark_len + 4])


def iter_im(im):
    for x in range(im.width):
        for y in range(im.height):
            yield x, y


def handle_mark(cbits, mark, bit):
    cbits.append(bit)
    if len(cbits) == 8:
        cbits.reverse()
        mark.append(int(''.join(map(str, cbits)), 2))
        cbits.clear()


if __name__ == '__main__':
    main()
