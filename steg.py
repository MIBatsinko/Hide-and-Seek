import os
from PIL import Image


class Stegano:
    def __init__(self):
        self.bits = []
        self.length = len(self.bits)

    #  opens image (*.bmp) as a container
    def open_container(self, img_steg_name):
        original = Image.open(img_steg_name)
        width, height = original.size
        self.rgb_im = original.convert('RGB')
        self.container = Image.new('RGB', (width, height))

    #  reads the secret file and write bit content into a list
    def read_secret(self, secret_name):
        with open(secret_name, 'rb') as f:
            byte = f.read(1)
            while byte:
                self.bits.extend('{:08b}'.format(ord(byte)))
                byte = f.read(1)

    #  opens the secret file
    def open_secret(self, file_name):
        self.bits = []  # здесь хранятся биты секретного файла
        self.read_secret(file_name)
        self.length = len(self.bits)
        if (self.length > (self.width * self.height)):
            return 0
        else:
            return 1

    #  output the max valid size of the secret file
    def max_size(self):
        return str((self.width * self.height) // 8)

    #  output size of the secret file
    def secret_size(self):
        return str(os.path.getsize(self.sec_file_name))

    # created a key
    def create_key(self, path_out):
        path_out = path_out[::-1].replace("pmb.", "", 1)
        path = path_out[::-1] + "_key.stg"
        with open(path, 'wt') as f:  # создаем ключ, в котором храним размер файла и его имя
            f.write(str(self.length))
            f.write('\n')
            f.write(self.sec_file_name.split('.', 1)[-1])

    #  main function of steganographic
    def steg(self, path):
        idx = 0
        for i in range(self.width):
            for j in range(self.height):
                if idx < self.length:
                    r, g, b = self.rgb_im.getpixel((i, j))
                    if int(self.bits[idx]) == 0:

                        r &= 254  # red/green/blue = r/g/b
                    else:
                        r |= 1
                    self.container.putpixel((i, j), (r, g, b))
                    idx += 1
                else:
                    r, g, b = self.rgb_im.getpixel((i, j))
                    self.container.putpixel((i, j), (r, g, b))

            self.create_key(path + ".bmp")
            self.container.save(path + ".bmp")
