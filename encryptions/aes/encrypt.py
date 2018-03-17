import aes
import aes.galois
import aes.schedule


def encrypt(msg: bytearray, key: bytearray):
    local_msg = msg[:]
    local_key = key[:]

    blocks_count = len(local_msg) // 16
    blocks = [local_msg[idx * aes.BLOCK_SIZE:(idx + 1) * aes.BLOCK_SIZE] for idx in range(blocks_count)]

    encryption = bytearray()
    for block in blocks:
        encryption.extend(encrypt_block(block, local_key))

    return encryption


def encrypt_block(msg_block: bytearray, key: bytearray):
    key_expanded = aes.schedule.expand_key(key)

    state = [[0] * aes.BLOCK_SIDE_SIZE for _idx in range(aes.BLOCK_SIDE_SIZE)]
    # заполнение state слева направо сверху вниз
    for idx, byte in enumerate(msg_block):
        state[idx % aes.BLOCK_SIDE_SIZE][idx // aes.BLOCK_SIDE_SIZE] = byte

    key_round = aes.schedule.create_round_key(key_expanded, 0)
    add_round_key(state, key_round)

    for i in range(1, aes.Nr):
        key_round = aes.schedule.create_round_key(key_expanded, i)
        aes_round(state, key_round)
    # final round - leave out the mixColumns transformation
    key_round = aes.schedule.create_round_key(key_expanded, aes.Nr)
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, key_round)

    res = bytearray()
    for column in range(aes.BLOCK_SIDE_SIZE):
        for row in range(aes.BLOCK_SIDE_SIZE):
            res.append(state[row][column])

    return res


def aes_round(state, round_key):
    sub_bytes(state)
    shift_rows(state)
    mix_columns(state)
    add_round_key(state, round_key)


def sub_bytes(state: list):
    for row in state:
        for idx, byte in enumerate(row):
            row[idx] = aes.sbox[byte]


def shift_rows(state: list):
    # 1 строка
    state[1].append(state[1].pop(0))
    # 2 строка
    state[2].append(state[2].pop(0))
    state[2].append(state[2].pop(0))
    # 3 строка
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))
    state[3].append(state[3].pop(0))


def mix_columns(state: list):
    for c in range(len(state)):
        column = aes.column_get(state, c)
        aes.galois.mix_column(column, aes.galois.poly)
        aes.column_set(state, c, column)


def add_round_key(state: list, round_key: list):
    for column in range(aes.BLOCK_SIDE_SIZE):
        for row in range(aes.BLOCK_SIDE_SIZE):
            state[row][column] ^= round_key[column * aes.BLOCK_SIDE_SIZE + row]
