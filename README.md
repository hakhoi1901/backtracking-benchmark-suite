# Báo cáo Thực nghiệm: Cài đặt và Tối ưu hóa Thuật toán Backtracking

**Sinh viên thực hiện:** 24120348 - Hà Đăng Khôi

**Môn học:** Tư duy tính toán

---

## Phương pháp Đo lường Hiệu năng

Để đảm bảo các số liệu thực nghiệm có cơ sở khoa học và phản ánh đúng bản chất của thuật toán, Benchmark được thiết kế dựa trên 3 nguyên tắc:

1. **Sử dụng Monotonic Clock:** Hệ thống sử dụng `time.perf_counter()` của thư viện chuẩn. Đây là bộ đếm có độ phân giải cao nhất ở cấp độ phần cứng. Khác với đồng hồ hệ thống, nó tuyệt đối không bị ảnh hưởng bởi các tiến trình đồng bộ thời gian ngầm của hệ điều hành, giúp kết quả đo đạc chính xác đến mức micro-giây mà không bị nhiễu.

2. **Đánh giá Trung bình:** Thời gian chạy của Backtracking phụ thuộc rất mạnh vào dữ liệu đầu vào (điểm xuất phát). Để tránh việc thuật toán vô tình rơi vào trường hợp tốt nhất (Best-case) hoặc xấu nhất (Worst-case), hệ thống sinh ra $K$ bộ cấu hình đầu vào ngẫu nhiên. Kết quả cuối cùng là trung bình cộng thời gian của $K$ lần chạy, phản ánh gần chính xác hiệu suất thực tế.

3. **Kiểm soát tính công bằng:** Cả hai thuật toán (Cơ bản và Tối ưu) được yêu cầu giải quyết **chính xác cùng một bộ dữ liệu test**. Đầu vào ngẫu nhiên được sinh ra và lưu lại trước khi test. Việc ép buộc hai thuật toán chạy trên cùng một tập tọa độ $(x, y)$ giúp loại bỏ hoàn toàn yếu tố may mắn.

4. **Kiểm soát Overhead đo lường:** Để thiết lập cơ chế ngắt thời gian (Time Limit = 20s) mà không làm chậm thuật toán, bộ đếm không gọi hàm kiểm tra hệ thống ở mọi bước đệ quy. Thay vào đó, bộ đếm sử dụng kỹ thuật "chunking" (chỉ xem đồng hồ 1 lần sau mỗi 1000 lần rẽ nhánh). Thiết kế này triệt tiêu độ trễ (overhead) của việc đo lường, đảm bảo tốc độ ghi nhận phản ánh đúng năng lực tính toán thuần túy của bản thân thuật toán.

---

## Phần 1: Bài toán 1 - Mã đi tuần

### 1. Mô tả bài toán
Tìm một hành trình cho quân Mã đi qua tất cả các ô trên bàn cờ kích thước $N \times N$, mỗi ô đúng một lần.

### 2. Phân tích Thuật toán
**a. Thuật toán Cơ bản (Brute-force Backtracking)**
* **Cơ chế:** Thử lần lượt 8 hướng di chuyển theo một thứ tự cố định. Nếu bước đi hợp lệ, đệ quy đi tiếp. Nếu gặp ngõ cụt, quay lui (trả lại trạng thái ô trống) và thử hướng khác.
* **Độ phức tạp:** $O(8^{N^2})$ trong trường hợp xấu nhất. Thời gian chạy phụ thuộc rất lớn vào vị trí xuất phát do duyệt cây theo đệ quy.

**b. Thuật toán Cải tiến (Warnsdorff's Heuristic)**
* **Cơ chế:** Tại mỗi bước, tính "bậc" (số lượng ô láng giềng hợp lệ có thể đi tiếp) của tất cả các ô đích tiềm năng. Sắp xếp các hướng đi ưu tiên bước vào những ô có bậc nhỏ nhất.
* **Bản chất tối ưu:** Giải quyết bài toán theo hướng "khó làm trước". Các ô ở góc/cạnh bàn cờ có ít đường vào sẽ được ưu tiên lấp đầy sớm, tránh việc chúng bị kẹt lại ở cuối hành trình và tạo ra ngõ cụt buộc thuật toán phải quay lui từ độ sâu lớn.

### 3. Kết quả Thực nghiệm (Average-case Analysis)
*Dữ liệu được đo đạc trung bình trên 5 điểm xuất phát ngẫu nhiên. Ngưỡng thời gian (Time Limit) là 20.0s.*

| Thuật toán | N | Tgian TB (ms) | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Optimized** | 4 | 2.35 | Có ca vô nghiệm |
| **Basic** | 4 | 1.82 | Có ca vô nghiệm |
| **Optimized** | 5 | 447.15 | Có ca vô nghiệm |
| **Basic** | 5 | 1107.39| Có ca vô nghiệm |
| **Optimized** | 6 | 0.73 | **Thành công** |
| **Basic** | 6 | Bỏ qua | Bị ngắt (> 20.0s) |
| **Optimized** | 8 | 2.94 | **Thành công** |
| **Basic** | 8 | Bỏ qua | Bị ngắt (> 20.0s) |
| **Optimized** | 20 | 370.11 | **Thành công** |
| **Basic** | 20 | Bỏ qua | Bị ngắt (> 20.0s) |
| **Optimized** | 50 | 5393.69| **Thành công** |
| **Basic** | 50 | Bỏ qua | Bị ngắt (> 20.0s) |
| **Optimized** | 100| Bỏ qua | Bị ngắt (> 20.0s) |
| **Basic** | 100| Bỏ qua | Bị ngắt (> 20.0s) |
| **Optimized** | 200| Bỏ qua | Bị ngắt (> 20.0s) |
| **Basic** | 200| Bỏ qua | Bị ngắt (> 20.0s) |

### 4. Giải thích và Phân tích Kết quả

Từ bảng dữ liệu khi mở rộng hệ thống lên mức độ lớn ($N=20$ đến $N=200$), ta rút ra được các kết luận cốt lõi về bản chất tối ưu:

* Bắt đầu từ $N=6$ trở đi, không gian trạng thái đã đủ lớn để thuật toán đệ quy (Basic) hoàn toàn lạc lối. Nó vượt quá giới hạn 20 giây và bị hệ thống ngắt toàn bộ ở các kích thước lớn hơn.
* Thuật toán Optimized giải quyết xuất sắc các bàn cờ cỡ vừa và lớn (từ $N=6$ đến $N=50$). La bàn Warnsdorff giúp nó đi thẳng đến đích mà gần như không rẽ nhánh sai.
    * Tuy nhiên, **tại sao Optimized lại thất bại ở $N=100$ và $N=200$?** Bản chất nằm ở chi phí chìm (Hidden Overhead) của hàm cắt tỉa `has_orphan_cell`. Để kiểm tra ô mồ côi, hàm này phải duyệt qua toàn bộ $N^2$ ô trên bàn cờ ở **mỗi bước đi**. Để đi hết bàn cờ $100 \times 100$, thuật toán phải gọi hàm kiểm tra này 10,000 lần. Suy ra, tổng số phép tính chỉ riêng cho việc cắt tỉa là $O(N^4)$ (khoảng $10^8$ phép lặp). Khối lượng tính toán này khiến nó bị ngắt vì vượt quá 20 giây dù đi rất đúng hướng.

---

## Phần 2: Bài toán 2 - Magic Square

### 1. Mô tả bài toán
Điền các số từ $1$ đến $N^2$ vào ma trận $N \times N$ sao cho tổng các số trên mỗi hàng, mỗi cột và hai đường chéo chính đều bằng nhau (Hằng số ma thuật $M$). Yêu cầu **vét cạn (tìm TẤT CẢ)** các cấu hình hợp lệ.

### 2. Phân tích Thuật toán
**a. Thuật toán Cơ bản (Phương pháp Xiêm - Siamese Method)**
* **Cơ chế:** Thuật toán kiến thiết (Constructive). Đặt số 1 ở giữa hàng đầu, liên tục đi chéo lên Đông Bắc. Nếu va chạm (ô đã có số), đi thẳng xuống dưới 1 ô. Ma trận cuộn vòng như hình xuyến (Torus).
* **Đặc điểm:** Không phải Backtracking. Độ phức tạp $O(N^2)$. Chạy cực nhanh nhưng chỉ tìm được 1 nghiệm duy nhất và tê liệt với $N$ chẵn.

**b. Thuật toán Cải tiến (Backtracking + Bitmask + Pruning)**
* **Cơ chế:** Duyệt không gian trạng thái. Sử dụng một số nguyên `used_mask` để đánh dấu số đã dùng qua các phép toán Bitwise (`&`, `|`, `<<`) nhằm đạt tốc độ truy xuất $O(1)$ ở mức CPU.
* **Bản chất tối ưu (Branch & Bound):**
    * **Forward Checking (Dội trần):** Tính tổng tích lũy theo thời gian thực. Cắt nhánh ngay lập tức nếu tổng một hàng/cột/chéo vượt quá $M$.
    * **Chốt chặn cuối tuyến:** Khi điền đến ô cuối của một hàng/cột, nếu tổng không bằng chính xác $M$, từ chối nhánh đệ quy.

### 3. Kết quả Thực nghiệm
*Ngưỡng thời gian (Time Limit) được thiết lập là 20.0s.*

| Thuật toán | N | Số nghiệm | Tgian TB (ms) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **Optimized (Bitmask)**| 3 | **8** | 6.43 | Hoàn thành |
| **Basic (Siamese)** | 3 | **1** | 0.03 | Hoàn thành |
| **Optimized (Bitmask)**| 4 | N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 4 | 0 | < 0.005| Hoàn thành |
| **Optimized (Bitmask)**| 7 | N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 7 | **1** | 0.02 | Hoàn thành |
| **Optimized (Bitmask)**| 33 | N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 33 | **1** | 0.41 | Hoàn thành |
| **Optimized (Bitmask)**| 51 | N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 51 | **1** | 0.60 | Hoàn thành |
| **Optimized (Bitmask)**| 99 | N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 99 | **1** | 2.54 | Hoàn thành |
| **Optimized (Bitmask)**| 199| N/A | Bị ngắt (> 20.0s) | Bị ngắt |
| **Basic (Siamese)** | 199| **1** | 9.87 | Hoàn thành |

### 4. Giải thích và Phân tích Kết quả

Kết quả đo lường với các ma trận khổng lồ làm nổi bật rõ rệt hai trường phái tính toán:

* Ngay từ $N=4$, không gian tổ hợp đã bùng nổ lên $16!$ (hơn 20 nghìn tỷ hoán vị). Dù kỹ thuật Nhánh cận (Branch & Bound) kết hợp Bitmask có mạnh mẽ đến đâu, nó cũng không thể xuyên thủng màng lọc đệ quy này. Việc cố gắng đếm toàn bộ nghiệm của Ma phương bằng Backtracking ở các $N \ge 4$ là bất khả thi trên các hệ thống thông thường.
* Trái ngược với Backtracking, phương pháp Xiêm (Basic) hoàn toàn không rẽ nhánh. Độ phức tạp của nó là $O(N^2)$ (tỷ lệ thuận với số ô trên bàn cờ). 
    * Khi $N$ tăng từ 51 lên 199, số lượng ô tăng khoảng 16 lần ($2601$ lên $39601$ ô). Nhìn vào cột thời gian, ta thấy thời gian chạy cũng tăng theo tỷ lệ tương ứng (từ $0.60 \text{ ms}$ lên $\approx 9.87 \text{ ms}$). 
    * Điều này chứng minh tính ổn định tuyệt đối của các thuật toán có độ phức tạp đa thức (Polynomial Time). Dù bảng có lớn đến $199 \times 199$, thuật toán vẫn giải quyết mượt mà trong chưa tới $10 \text{ ms}$, nhưng phải đánh đổi bằng việc nó chỉ áp dụng được cho $N$ lẻ và chỉ tìm ra đúng 1 nghiệm duy nhất.

---

### Tổng kết Kỹ thuật
Sự tương phản ở $N=6$ (Mã đi tuần) và $N=4$ (Ma phương) làm nổi bật bản chất của thiết kế thuật toán:
* Phương pháp Heuristic (như Warnsdorff) là một **la bàn** dẫn hướng cực tốt để tìm ra 1 nghiệm trong không gian sâu.
* Cắt tỉa nhánh cận (Branch and Bound) là một **màng lọc** tốt, nhưng khi không gian mẫu bùng nổ theo hàm Giai thừa ($O(N^2!)$), màng lọc cũng bị thủng. Với bài toán vét cạn tất cả tập nghiệm, Backtracking có giới hạn thực tiễn rất thấp.
* Thuật toán kiến thiết toán học (Siamese) luôn có độ trễ bằng 0, nhưng phải đánh đổi bằng sự cứng nhắc (không duyệt được toàn bộ trạng thái, không chạy được mọi đầu vào).