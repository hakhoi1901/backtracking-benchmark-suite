import time

def knights_tour_optimized(n, start_x=0, start_y=0, time_limit=None):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    start_time = time.perf_counter()
    calls = 0

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1

    def count_onward_moves(x, y):
        """Đếm số lượng ô hợp lệ có thể đi tiếp từ tọa độ (x, y)"""
        count = 0
        for dx, dy in moves:
            if is_valid(x + dx, y + dy):
                count += 1
        return count

    def has_orphan_cell(step):
        """
        Điều kiện đúng: Chỉ kiểm tra mồ côi khi số ô còn lại > 1.
        Khi step = n*n - 2, ta vừa đặt ô thứ n*n - 1, bàn cờ chỉ còn 1 ô trống.
        """
        if step >= n * n - 2: # Sửa -1 thành -2
            return False
            
        for r in range(n):
            for c in range(n):
                if board[r][c] == -1:
                    if count_onward_moves(r, c) == 0:
                        return True
        return False

    def solve(x, y, step):
        nonlocal calls
        
        calls += 1
        if time_limit and calls % 1000 == 0:
            if time.perf_counter() - start_time > time_limit:
                raise TimeoutError("Vượt quá thời gian cho phép")

        if step == n * n:
            return True

        # Kỹ thuật Warnsdorff: Lấy các nước đi hợp lệ và tính toán bậc (degree)
        valid_next_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                degree = count_onward_moves(nx, ny)
                valid_next_moves.append((degree, nx, ny))

        # Warnsdorff's Rule: Sắp xếp ưu tiên các ô có ít nước đi tiếp theo nhất (tham lam)
        valid_next_moves.sort(key=lambda item: item[0])

        for degree, nx, ny in valid_next_moves:
            board[nx][ny] = step
            
            # Pruning: Chỉ tiếp tục đệ quy nếu không tạo ra ô mồ côi
            if not has_orphan_cell(step):
                if solve(nx, ny, step + 1):
                    return True
                    
            board[nx][ny] = -1 # Backtrack

        return False

    board[start_x][start_y] = 0
    if solve(start_x, start_y, 1):
        return board
    return None

def print_board(board):
    if board is None:
        print("Khong tim thay loi giai")
        return
    for row in board:
        for cell in row:
            print(f"{cell:2}", end=" ")
        print()

if __name__ == "__main__":
    result = knights_tour_optimized(8, 0, 0)
    print_board(result)