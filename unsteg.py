from PIL import Image
from itertools import zip_longest


class Unstegano:
    def __init__(self):
        self.bits = []
        self.length = len(self.bits)

    #  opens image (*.bmp) as a container
    def open_container(self, img_steg_name):
        original = Image.open(img_steg_name)
        width, height = original.size
        self.rgb_im = original.convert('RGB')
        self.container = Image.new('RGB', (width, height))

    #  opens the key
    def open_key(self, key_name):
        key = open(key_name, 'rt')
        self.length = int(key.readline().strip('\n'))
        self.sec_file_name = key.readline()

    # main function of the recovery the secret file from the container
    def unsteg(self):
        bit_sequence = ""
        self.bits = []
        idx = 0
        for i in range(self.width):
            for j in range(self.height):
                if idx < self.length:
                    r, g, b = self.rgb_im.getpixel((i, j))
                    # r &= 1#red/green/blue = r/g/b
                    if (r & 1) == 0:
                        r = 0  # red/green/blue = r/g/b
                    else:
                        r = 1
                    bit_sequence += str(r)
                    idx += 1
        for i in bit_sequence:
            self.bits.append(i)

    #  saves the bitwise recovered file
    def save_output(self, path):
        with open(path + "." + self.sec_file_name, 'wb') as f:
            f.write(bytearray(int(''.join(x), 2) for x in self.grouper(self.bits, 8)))

    #  groups the bits into bytes
    def grouper(self, iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)
