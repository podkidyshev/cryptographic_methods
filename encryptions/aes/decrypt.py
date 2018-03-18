import aes.galois
import aes.schedule


def decrypt(msg, key):
    local_msg = msg[:]
    local_key = key[:]

    blocks_count = len(local_msg) // 16
    blocks = [local_msg[idx * aes.BLOCK_SIZE:(idx + 1) * aes.BLOCK_SIZE] for idx in range(blocks_count)]

    decryption = bytearray()
    for block in blocks:
        decryption.extend(decrypt_block(block, local_key))

    return decryption


def decrypt_block(msg_block: bytearray, key: bytearray):
    key_expanded = aes.schedule.expand_key(key)

    state = [[0] * aes.BLOCK_SIDE_SIZE for _idx in range(aes.BLOCK_SIDE_SIZE)]
    # заполнение state слева направо сверху вниз
    for idx, byte in enumerate(msg_block):
        state[idx % aes.BLOCK_SIDE_SIZE][idx // aes.BLOCK_SIDE_SIZE] = byte

    key_round = aes.schedule.create_round_key(key_expanded, aes.Nr)
    add_round_key_inv(state, key_round)
    shift_rows_inv(state)
    sub_bytes_inv(state)
    for i in range(aes.Nr - 1, 0, -1):
        key_round = aes.schedule.create_round_key(key_expanded, i)
        aes_round_inv(state, key_round)
    # final round - leave out the mixColumns transformation
    key_round = aes.schedule.create_round_key(key_expanded, 0)
    add_round_key_inv(state, key_round)

    res = bytearray()
    for column in range(aes.BLOCK_SIDE_SIZE):
        for row in range(aes.BLOCK_SIDE_SIZE):
            res.append(state[row][column])

    return res


def aes_round_inv(state, key_round):
    add_round_key_inv(state, key_round)
    mix_columns_inv(state)
    shift_rows_inv(state)
    sub_bytes_inv(state)


def sub_bytes_inv(state: list):
    for row in state:
        for idx, byte in enumerate(row):
            row[idx] = aes.sbox_inv[byte]


def shift_rows_inv(state):
    # 1 строка
    state[1].insert(0, state[1].pop())
    # 2 строка
    state[2].insert(0, state[2].pop())
    state[2].insert(0, state[2].pop())
    # 3 строка
    state[3].insert(0, state[3].pop())
    state[3].insert(0, state[3].pop())
    state[3].insert(0, state[3].pop())


def mix_columns_inv(state):
    for c in range(len(state)):
        column = aes.column_get(state, c)
        aes.galois.mix_column(column, aes.galois.poly_inv)
        aes.column_set(state, c, column)


def add_round_key_inv(state: list, round_key: list):
    for column in range(aes.BLOCK_SIDE_SIZE):
        for row in range(aes.BLOCK_SIDE_SIZE):
            state[row][column] ^= round_key[column * aes.BLOCK_SIDE_SIZE + row]
