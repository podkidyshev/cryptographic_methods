import aes
import aes.encrypt
import aes.decrypt

DEFAULT_KEY = '5468617473206D79204B756E67204675'  # '3abcf64353247362432948732'
DEFAULT_MSG = 'Two One Nine TwoTwo One'  # 'hey hello world!'


def main():
    key_str = DEFAULT_KEY  # input('Введите ключ: ')
    msg_str = DEFAULT_MSG  # input('Введите сообщение: ')

    key_bytes = aes.handle_key(key_str)
    msg_bytes = aes.handle_message(msg_str)

    print('Ключ: ', key_bytes)
    print('Сообщение: ', msg_bytes)
    encryption = aes.encrypt.encrypt(msg_bytes, key_bytes)

    assert len(encryption) == len(msg_bytes)

    print('Зашифрованное сообщение: ', end='')
    aes.print_in_hex(encryption)
    decryption = aes.decrypt.decrypt(encryption, key_bytes)
    print('Расшифрованное сообщение: ', decryption)


if __name__ == '__main__':
    main()
