import json
import aes
import aes.encrypt
import aes.decrypt


def handle_send(msg: str, key_out=None, **kwargs):
    msg_local = msg.encode('utf-8') if key_out is None else aes.encrypt.encrypt(aes.handle_message(msg), key_out)

    pack = kwargs
    pack['len'] = len(msg)
    pack['msg'] = msg_local
    if key_out is not None:
        pack['encrypted'] = True

    return json.dumps(pack).encode('utf-8')


def handle_receive(msg: bytearray, key_in=None):
    pack = json.loads(msg, encoding='utf-8')

    if key_in is not None:
        pack['msg'] = aes.decrypt.decrypt(pack['msg'], key_in)

    pack['msg'] = pack['msg'].decode('utf-8')[:pack['len']]

    return pack['msg']
