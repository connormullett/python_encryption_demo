
import os
import random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = "_encrypted_" + filename
    file_size = str(os.path.getsize(filename)).zfill(16).encode('utf-8')
    iv = os.urandom(16)

    encrypter = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, 'rb') as in_f:
        with open(output_file, 'wb') as out_f:
            out_f.write(file_size)
            out_f.write(iv)

            while True:
                chunk = in_f.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode('utf-8') * (16 - (len(chunk) - 16))

                out_f.write(encrypter.encrypt(chunk))


def decrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = '_decrypted_' + filename[11:]

    with open(filename, 'rb') as in_f:
        filesize = in_f.read(16)
        iv = in_f.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(output_file, 'wb') as out_f:
            while True:
                chunk = in_f.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_f.write(decryptor.decrypt(chunk))
            out_f.truncate(int(filesize))


def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


def main():
    choice = int(input('1. Encrypt\n2. Decrypt\n'))
    if choice == 1:
        filename = input('file to encrypt: ')
        password = input('password: ')
        encrypt(get_key(password), filename)
        print('Done')
    elif choice == 2:
        filename = input('file to decrypt: ')
        password = input('password: ')
        decrypt(get_key(password), filename)
        print('done')
    else:
        print('invalid input')


if __name__ == '__main__':
    main()
