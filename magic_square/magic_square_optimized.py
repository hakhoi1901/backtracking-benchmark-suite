import time

def magic_square_optimized(n=3, time_limit=None):
    M = n * (n * n + 1) // 2
    
    solution_count = 0
    board = [0] * (n * n)
    row_sum = [0] * n
    col_sum = [0] * n
    diag1_sum = 0
    diag2_sum = 0
    
    saved_boards = []

    start_time = time.perf_counter()
    calls = 0

    def solve_fast(index, used_mask):
        nonlocal solution_count, diag1_sum, diag2_sum, calls

        calls += 1
        if time_limit and calls % 1000 == 0:
            if time.perf_counter() - start_time > time_limit:
                raise TimeoutError("Vượt quá thời gian cho phép")

        if index == n * n:
            solution_count += 1
            if len(saved_boards) < 2:
                saved_boards.append(list(board)) 
            return

        r = index // n
        c = index % n

        for num in range(1, n * n + 1):
            if (used_mask & (1 << num)) == 0:
                # Nhánh cận 1: Dội trần
                if row_sum[r] + num > M: continue
                if col_sum[c] + num > M: continue
                if r == c and diag1_sum + num > M: continue
                if r + c == n - 1 and diag2_sum + num > M: continue

                # Nhánh cận 2: Chốt kiểm tra cuối tuyến
                if c == n - 1 and row_sum[r] + num != M: continue
                if r == n - 1 and col_sum[c] + num != M: continue
                if r == n - 1 and c == n - 1 and diag1_sum + num != M: continue
                if r == n - 1 and c == 0 and diag2_sum + num != M: continue

                # Cập nhật trạng thái
                board[index] = num
                row_sum[r] += num
                col_sum[c] += num
                if r == c: diag1_sum += num
                if r + c == n - 1: diag2_sum += num

                # Đệ quy
                solve_fast(index + 1, used_mask | (1 << num))

                # Quay lui
                row_sum[r] -= num
                col_sum[c] -= num
                if r == c: diag1_sum -= num
                if r + c == n - 1: diag2_sum -= num

    solve_fast(0, 0)
    return solution_count, saved_boards