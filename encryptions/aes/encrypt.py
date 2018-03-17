import aes


def encrypt(msg: bytearray, key: bytearray):
    local_msg = msg[:]
    local_key = key[:]

    blocks_count = len(local_msg) // 16
    blocks = [local_msg[idx:idx + aes.BLOCK_SIZE] for idx in range(blocks_count)]

    encryption = bytearray()
    for block in blocks:
        encryption.extend(encrypt_block(block, local_key))

    return encryption


def encrypt_block(msg_block: bytearray, key: bytearray):
    len_state = int(aes.BLOCK_SIZE ** 0.5)
    state = [[0] * len_state for _idx in range(len_state)]
    # заполнение state слева направо сверху вниз
    for idx, byte in enumerate(msg_block):
        state[idx % len_state][idx // len_state] = byte

    for _idx in range(aes.Nr - 1):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state)

    return []


def sub_bytes(state: list):
    for row in state:
        for idx, byte in enumerate(row):
            row[idx] = aes.sbox[aes.high(byte)][aes.low(byte)]


def shift_rows(state: list):
    # 1 строка
    state[1].insert(state[1].pop())
    # 2 строка
    state[2].insert(state[2].pop())
    state[2].insert(state[2].pop())
    # 3 строка
    state[3].insert(state[3].pop())
    state[3].insert(state[3].pop())
    state[3].insert(state[3].pop())


def mix_columns(state: list):
    for c in range(len(state)):
        column = aes.column_get(state, c)

        aes.column_set(state, c, column)


def add_round_key(state: list):
    pass
