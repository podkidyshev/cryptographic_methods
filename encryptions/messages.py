import json
import aes
import aes.encrypt
import aes.decrypt


def handle_send(msg: str, key_out=None, **kwargs):
    msg_local = msg.encode('utf-8') if key_out is None else aes.encrypt.encrypt(aes.handle_message(msg), key_out)

    pack = kwargs
    pack['len'] = len(msg)
    pack['msg'] = str(msg_local)
    if key_out is not None:
        print('Отправлена криптограмма: ', end='')
        aes.print_in_hex(msg_local)
        pack['encrypted'] = True

    return json.dumps(pack).encode('utf-8')


def handle_receive(msg: bytearray, key_in=None):
    pack = json.loads(msg, encoding='utf-8')
    # костыль
    pack['msg'] = eval(pack['msg'])

    if 'encrypted' in pack:
        print('Принята криптограмма ', end='')
        aes.print_in_hex(pack['msg'])
        pack['msg'] = aes.decrypt.decrypt(pack['msg'], key_in)

    pack['msg'] = pack['msg'].decode('utf-8')[:pack['len']]

    return pack
