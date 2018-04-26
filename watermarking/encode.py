import sys
from PIL import Image


def main():
    assert len(sys.argv) == 3, 'Передайте файл изображения и файл для подписи'

    file_image = sys.argv[1]
    file_mark = sys.argv[2]

    im = Image.open(file_image)
    with open(file_mark, 'rb') as f_mark:
        mark = f_mark.read()

    mark = len(mark).to_bytes(4, byteorder='big') + bytearray(mark)
    iter_mark(mark)

    for (x, y), bit in zip(iter_im(im), iter_mark(mark)):
        pixel = im.getpixel((x, y))
        pixel = (int(bin(pixel[0])[:-1] + str(bit), 2), *pixel[1:])
        im.putpixel((x, y), pixel)

    im.save('marked_{}'.format(file_image))


def iter_mark(mark):
    for byte in mark:
        for _idx in range(8):
            yield byte % 2
            byte //= 2


def iter_im(im):
    for x in range(im.width):
        for y in range(im.height):
            yield x, y


if __name__ == '__main__':
    main()
