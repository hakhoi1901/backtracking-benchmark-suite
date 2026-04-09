import time

def magic_square_basic(n):

    if n % 2 == 0:
        return 0, []

    magic_square = [[0] * n for _ in range(n)]

    i = 0
    j = n // 2

    for num in range(1, n * n + 1):
        magic_square[i][j] = num
        
        next_i = (i - 1) % n
        next_j = (j + 1) % n

        if magic_square[next_i][next_j] != 0:
            i = (i + 1) % n
        else:
            i = next_i
            j = next_j

    flattened_board = [cell for row in magic_square for cell in row]

    return 1, [flattened_board]