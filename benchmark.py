import time
import os
import random

from knight_tour.knight_tour_basic import knights_tour_basic
from knight_tour.knight_tour_optimized import knights_tour_optimized

from magic_square.magic_square_basic import magic_square_basic
from magic_square.magic_square_optimized import magic_square_optimized


def measure_time(func, *args, **kwargs):
    """Đo thời gian chạy và quản lý trạng thái Timeout."""
    start_time = time.perf_counter()
    try:
        result = func(*args, **kwargs)
        status = "Success"
    except TimeoutError:
        result = None
        status = "Timeout"
    end_time = time.perf_counter()
    
    return result, status, (end_time - start_time) * 1000

def generate_random_starts(n, num_trials):
    start_points = []
    for _ in range(num_trials):
        start_points.append((random.randint(0, n - 1), random.randint(0, n - 1)))
    return start_points

def write_knight_tour_to_log(n, board, algo_name, sx, sy, filename="log.txt"):
    """Hàm ghi log chuyên dụng cho mảng 2 chiều của Knight Tour"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n[{algo_name}] --- MÃ ĐI TUẦN {n}x{n} (Bắt đầu: {sx},{sy}) ---\n")
        if board is None:
            f.write(">> Vô nghiệm.\n")
        else:
            for row in board:
                for cell in row:
                    f.write(f"{cell:3} ")
                f.write("\n")
        f.write("-" * 35 + "\n")

def write_boards_to_log(n, boards, algo_name, filename="log.txt"):
    """Hàm phụ trợ định dạng 1D array thành ma trận 2D và ghi file"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n[{algo_name}] --- MA PHƯƠNG {n}x{n} ---\n")
        if not boards:
            f.write("Không tìm thấy nghiệm nào.\n")
            
        for idx, b in enumerate(boards):
            f.write(f">> Nghiệm mẫu {idx + 1}:\n")
            for i in range(n * n):
                f.write(f"{b[i]:3} ")
                if (i + 1) % n == 0:
                    f.write("\n")
            f.write("-" * 20 + "\n")


def run_knight_tour_benchmark(test_cases, time_limit, num_trials=3):
    print("\n" + "="*80)
    print(f"[{'KNIGHT TOUR BENCHMARK':^76}]")
    print("="*80)
    print("Đang ghi kết quả chi tiết ra file 'log.txt'...")
    print(f"Đang chạy đo lường trung bình với {num_trials} điểm ngẫu nhiên mỗi N...")
    print(f"{'Thuật toán':<25} | {'N':<5} | {'Điểm test':<10} | {'Tgian TB (ms)':<15} | {'Trạng thái'}")
    print("-" * 80)
    
    timeout_str = f"> {int(time_limit * 1000)}"
    
    for n in test_cases:
        start_points = generate_random_starts(n, num_trials)
        
        # --- Chạy Optimized ---
        total_time_opt = 0
        success_opt = True
        is_timeout_opt = False
        
        for sx, sy in start_points:
            res_opt, status, t = measure_time(knights_tour_optimized, n, sx, sy, time_limit=time_limit)
            
            if status == "Timeout":
                is_timeout_opt = True
                break
                
            total_time_opt += t
            if res_opt is None: 
                success_opt = False
            write_knight_tour_to_log(n, res_opt, "Optimized", sx, sy)
                
        if is_timeout_opt:
            print(f"{'Optimized (Warnsdorff)':<25} | {n:<5} | {num_trials:<10} | {timeout_str:<15} | Bị ngắt (Quá {time_limit}s)")
        else:
            print(f"{'Optimized (Warnsdorff)':<25} | {n:<5} | {num_trials:<10} | {total_time_opt/num_trials:<15.4f} | {'Thành công' if success_opt else 'Có ca vô nghiệm'}")
        
        # --- Chạy Basic ---
        total_time_basic = 0
        success_basic = True
        is_timeout_basic = False
        
        for sx, sy in start_points:
            res_basic, status, t = measure_time(knights_tour_basic, n, sx, sy, time_limit=time_limit)
            
            if status == "Timeout":
                is_timeout_basic = True
                break
                
            total_time_basic += t
            if res_basic is None: 
                success_basic = False
            write_knight_tour_to_log(n, res_basic, "Basic", sx, sy)
                
        if is_timeout_basic:
            print(f"{'Basic (Backtracking)':<25} | {n:<5} | {num_trials:<10} | {timeout_str:<15} | Bị ngắt (Quá {time_limit}s)")
        else:
            print(f"{'Basic (Backtracking)':<25} | {n:<5} | {num_trials:<10} | {total_time_basic/num_trials:<15.4f} | {'Thành công' if success_basic else 'Có ca vô nghiệm'}")
        
        print("-" * 80)


def run_magic_square_benchmark(test_cases, time_limit):
    print("\n" + "="*80)
    print(f"[{'MAGIC SQUARE BENCHMARK':^76}]")
    print("="*80)
    print(f"{'Thuật toán':<25} | {'N':<5} | {'Số nghiệm':<10} | {'Tgian TB (ms)':<15} | {'Trạng thái'}")
    print("-" * 80)
    
    timeout_str = f"> {int(time_limit * 1000)}"
    
    for n in test_cases:
        res_opt, status_opt, time_opt = measure_time(magic_square_optimized, n, time_limit=time_limit)
        
        if status_opt == "Timeout":
            print(f"{'Optimized (Bitmask)':<25} | {n:<5} | {'-':<10} | {timeout_str:<15} | Bị ngắt (Quá {time_limit}s)")
        else:
            count_opt, boards_opt = res_opt
            write_boards_to_log(n, boards_opt, "Optimized", "log.txt")
            print(f"{'Optimized (Bitmask)':<25} | {n:<5} | {count_opt:<10} | {time_opt:<15.4f} | Hoàn thành")

        res_basic, status_basic, time_basic = measure_time(magic_square_basic, n)
        count_basic, boards_basic = res_basic
        write_boards_to_log(n, boards_basic, "Basic", "log.txt")
        print(f"{'Basic (Siamese)':<25} | {n:<5} | {count_basic:<10} | {time_basic:<15.4f} | Hoàn thành")
        
        print("-" * 80)

if __name__ == "__main__":
    # Cấu hình không gian test
    KT_TEST_CASES = [4, 5, 6, 8] # Kích thước N cho Mã đi tuần
    MS_TEST_CASES = [3, 4, 5] # Kích thước N cho Ma phương
    
    TIME_LIMIT_SEC = 20.0 # Ngưỡng ngắt thuật toán (giây)
    NUM_TRIALS = 5 # Số lượng điểm xuất phát ngẫu nhiên
    
    LOG_FILE = "log.txt"

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    run_knight_tour_benchmark(test_cases=KT_TEST_CASES, 
                              time_limit=TIME_LIMIT_SEC, 
                              num_trials=NUM_TRIALS)
                              
    run_magic_square_benchmark(test_cases=MS_TEST_CASES, 
                               time_limit=TIME_LIMIT_SEC)