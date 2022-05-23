class AES:

    def __init__(self, message, key, zeroes=0):
        self.message = message
        self.key = key
        self.original_key = key
        self.zeroes = zeroes
        self.msg_save = ''

    @classmethod
    def parse_text(cls, text, key):
        text = ''.join(["%02X " % ord(x) for x in text]).strip().split(' ')

        if key == '0':
            import random

            key = ''
            for i in range(0, 16):
                key += str(random.randint(0, 128)) + ','

            key = key[:-1]

        entry_key = key.split(',')
        key = []

        for i in range(0, len(entry_key)):
            key.append(int(entry_key[i]))

        key = ''.join(["%02X " % x for x in key]).strip().split(' ')

        if len(text) < 16:
            text += (16 - len(text)) * '0'

        if len(key) < 16:
            key += (16 - len(key)) * '0'

        return AES(text, key)

    def add_round_key(self):
        for i in range(0, len(self.message)):
            self.message[i] = format(
                int(self.message[i], 16) ^ int(self.key[i], 16), 'x')

    def sub_bytes(self):
        for i in range(0, len(self.message)):
            self.message[i] = format(sbox[int(self.message[i], 16)], 'x')

    def shift_rows(self):
        for i in range(0, 4):
            temp_list = rotate([
                self.message[i], self.message[i + 4], self.message[i + 8],
                self.message[i + 12]
            ], i)
            for j in range(0, 4):
                self.message[i + j * 4] = temp_list[j]

    def mix_columns(self):
        new_message = list()
        for i in range(0, 4):
            for j in range(0, 4):
                total = 0
                for index in range(0, 4):
                    if mxc[j][index] == 2:
                        total ^= mult2[int(self.message[i * 4 + index], 16)]
                    elif mxc[j][index] == 3:
                        total ^= mult3[int(self.message[i * 4 + index], 16)]
                    else:
                        total ^= int(self.message[i * 4 + index], 16)
                new_message.append(format(total, 'x'))
        self.message = new_message

    def next_round_key(self, index):
        new_key = []
        w3 = rotate(self.key[12:16], 1)
        w3 = [format(sbox[int(item, 16)], 'x') for item in w3]
        w3[0] = format(int(w3[0], 16) ^ int(rc[index]), 'x')

        for i in range(0, 4):
            new_key.append(format(int(self.key[i], 16) ^ int(w3[i], 16), 'x'))
        for i in range(1, 4):
            for j in range(0, 4):
                new_key.append(
                    format(
                        int(self.key[i * 4 + j], 16)
                        ^ int(new_key[(i - 1) * 4 + j], 16), 'x'))

        self.key = new_key

    def next_key(self, index):
        self.key = self.original_key
        for i in range(index):
            self.next_round_key(i)

    def save_exit(self):
        for i in range(0, len(self.message)):
            if i % 4 == 0:
                self.msg_save += '\n'
            self.msg_save += '0x' + str(self.message[i]) + ' '

    def save_key(self):
        for i in range(0, len(self.original_key)):
            if i % 4 == 0:
                self.msg_save += '\n'
            self.msg_save += '0x' + str(self.original_key[i]) + ' '

    def encrypt(self):
        self.msg_save += '\n**** Texto simples ****\n'
        self.save_exit()

        self.add_round_key()
        self.msg_save += '\n\n**** AddRoundKey-Round 0 ****\n'
        self.save_exit()

        for i in range(0, 11):
            self.sub_bytes()
            self.msg_save += f'\n\n**** SubBytes-Round {i} ****\n'
            self.save_exit()

            self.shift_rows()
            self.msg_save += f'\n\n**** ShiftRows-Round {i} ****\n'
            self.save_exit()

            self.mix_columns()
            self.msg_save += f'\n\n**** MixedColumns-Round {i} ****\n'
            self.save_exit()

            self.next_round_key(i)

            self.add_round_key()
            self.msg_save += f'\n\n**** addRoundKey-Round {i} ****\n'
            self.save_exit()

            self.msg_save += f'\n\n**** Texto cifrado ****\n'
            self.save_exit()

        for i in range(len(self.message)):
            if len(self.message[i]) != 2:
                self.message[i] = '0' + self.message[i]

        self.key = self.original_key

        self.msg_save += f'\n\n**** Chave Original ****\n'
        self.save_key()

        return self.msg_save


def rotate(l, n):
    n = n % len(l)
    return l[n:] + l[:n]


mxc = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]

rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c]

sbox = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B,
    0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26,
    0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2,
    0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED,
    0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F,
    0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC,
    0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14,
    0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D,
    0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F,
    0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11,
    0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F,
    0xB0, 0x54, 0xBB, 0x16
]

mult2 = [
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16,
    0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e,
    0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 0x40, 0x42, 0x44, 0x46,
    0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e,
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76,
    0x78, 0x7a, 0x7c, 0x7e, 0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e,
    0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e, 0xa0, 0xa2, 0xa4, 0xa6,
    0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe,
    0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6,
    0xd8, 0xda, 0xdc, 0xde, 0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee,
    0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe, 0x1b, 0x19, 0x1f, 0x1d,
    0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05,
    0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d,
    0x23, 0x21, 0x27, 0x25, 0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55,
    0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45, 0x7b, 0x79, 0x7f, 0x7d,
    0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65,
    0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d,
    0x83, 0x81, 0x87, 0x85, 0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5,
    0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5, 0xdb, 0xd9, 0xdf, 0xdd,
    0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5,
    0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed,
    0xe3, 0xe1, 0xe7, 0xe5
]

mult3 = [
    0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09, 0x18, 0x1b, 0x1e, 0x1d,
    0x14, 0x17, 0x12, 0x11, 0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39,
    0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21, 0x60, 0x63, 0x66, 0x65,
    0x6c, 0x6f, 0x6a, 0x69, 0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71,
    0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59, 0x48, 0x4b, 0x4e, 0x4d,
    0x44, 0x47, 0x42, 0x41, 0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9,
    0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1, 0xf0, 0xf3, 0xf6, 0xf5,
    0xfc, 0xff, 0xfa, 0xf9, 0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1,
    0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9, 0xb8, 0xbb, 0xbe, 0xbd,
    0xb4, 0xb7, 0xb2, 0xb1, 0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99,
    0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81, 0x9b, 0x98, 0x9d, 0x9e,
    0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a,
    0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2, 0xb3, 0xb0, 0xb5, 0xb6,
    0xbf, 0xbc, 0xb9, 0xba, 0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2,
    0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea, 0xcb, 0xc8, 0xcd, 0xce,
    0xc7, 0xc4, 0xc1, 0xc2, 0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda,
    0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46,
    0x4f, 0x4c, 0x49, 0x4a, 0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62,
    0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a, 0x3b, 0x38, 0x3d, 0x3e,
    0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a,
    0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16,
    0x1f, 0x1c, 0x19, 0x1a
]


def main():
    from tkinter import Tk, filedialog

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Read text to encrypt
    open_file = filedialog.askopenfile(
        title='Selecione um arquivo para criptografar',
        defaultextension='[.txt, .bin]')

    entry_type = str(open_file.name)[-3:]

    if entry_type == 'txt':
        to_encrypt = open_file.read()
    else:
        to_encrypt = "".join(
            [chr(int(binary, 2)) for binary in open_file.read().split(" ")])

    # Read Key
    key = input("Entre com a chave ( 0 para chave aleatória ): ")

    aes = AES.parse_text(text=to_encrypt, key=key)
    encrypted_file = aes.encrypt()

    path = filedialog.asksaveasfile(defaultextension='.txt',
                                    initialfile='encrypted.txt',
                                    title='Salve o arquivo criptografado')

    file = open(path.name, 'w')
    file.write(encrypted_file)
    file.close()


if __name__ == '__main__':
    main()