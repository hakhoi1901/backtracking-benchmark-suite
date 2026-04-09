import time

def knights_tour_basic(n, start_x=0, start_y=0, time_limit=None):
    board = [[-1 for _ in range(n)] for _ in range(n)]

    # 8 hướng di chuyển có thể của quân mã
    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    start_time = time.perf_counter()
    calls = 0

    def is_valid(x, y):
        # Kiểm tra tọa độ có nằm trong bàn cờ và ô đó chưa được đi qua (-1)
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1

    def solve(x, y, step):
        nonlocal calls

        calls += 1
        if time_limit and calls % 1000 == 0:
            if time.perf_counter() - start_time > time_limit:
                raise TimeoutError("Vượt quá thời gian cho phép")
        
        # Nếu số bước bằng tổng số ô trên bàn cờ -> Đã đi hết
        if step == n * n:
            return True

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                # Thử đi nước này
                board[nx][ny] = step

                # Đệ quy đi tiếp nước sau
                if solve(nx, ny, step + 1):
                    return True

                # Backtrack: Nếu đi hướng này không dẫn đến kết quả, quay lui (trả lại -1)
                board[nx][ny] = -1
        return False

    # Khởi tạo vị trí bắt đầu
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
            # Format để in ra ma trận căn lề đều đặn
            print(f"{cell:2}", end=" ")
        print()

if __name__ == "__main__":
    # Thực thi thử nghiệm với bàn cờ 5x5, bắt đầu tại (0,0)
    result = knights_tour_basic(5, 0, 0)
    print_board(result)