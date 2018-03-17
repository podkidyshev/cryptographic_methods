import aes
import aes.encrypt

DEFAULT_KEY = '3abcf643532'
DEFAULT_MSG = 'hey hello world!'


def main():
    key_str = DEFAULT_KEY  # input('Введите ключ: ')
    msg_str = DEFAULT_MSG  # input('Введите сообщение: ')

    key_bytes = aes.handle_key(key_str)
    msg_bytes = aes.handle_message(msg_str)

    print(aes.encrypt.encrypt(msg_bytes, key_bytes))


if __name__ == '__main__':
    main()
