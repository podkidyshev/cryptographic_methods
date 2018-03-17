import aes.galois


def decrypt(msg, key):
    pass


def mix_columns_inv(state):
    for i in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j * 4 + i])

        # apply mixColumn on our virtual column
            aes.galois.mix_column_inv(column)

        # transfer the new values back into the state table
        for j in range(4):
            state[j * 4 + i] = column[j]
