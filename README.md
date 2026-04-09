# Báo cáo Thực nghiệm: Cài đặt và Tối ưu hóa Thuật toán Backtracking

**Sinh viên thực hiện:** 24120348 - Hà Đăng Khôi

**Môn học:** Tư duy tính toán

---

## Phương pháp Đo lường Hiệu năng

Để đảm bảo các số liệu thực nghiệm có cơ sở khoa học và phản ánh đúng bản chất của thuật toán, Benchmark được thiết kế dựa trên 3 nguyên tắc:

1. **Sử dụng Monotonic Clock:** Hệ thống sử dụng `time.perf_counter()` của thư viện chuẩn. Đây là bộ đếm có độ phân giải cao nhất ở cấp độ phần cứng. Khác với đồng hồ hệ thống, nó tuyệt đối không bị ảnh hưởng bởi các tiến trình đồng bộ thời gian ngầm của hệ điều hành, giúp kết quả đo đạc chính xác đến mức micro-giây mà không bị nhiễu.

2. **Đánh giá Trung bình:** Thời gian chạy của Backtracking phụ thuộc rất mạnh vào dữ liệu đầu vào (điểm xuất phát). Để tránh việc thuật toán vô tình rơi vào trường hợp tốt nhất (Best-case) hoặc xấu nhất (Worst-case), hệ thống sinh ra $K$ bộ cấu hình đầu vào ngẫu nhiên. Kết quả cuối cùng là trung bình cộng thời gian của $K$ lần chạy, phản ánh gần chính xác hiệu suất thực tế.

3. **Kiểm soát tính công bằng:** Cả hai thuật toán (Cơ bản và Tối ưu) được yêu cầu giải quyết **chính xác cùng một bộ dữ liệu test**. Đầu vào ngẫu nhiên được sinh ra và lưu lại trước khi test. Việc ép buộc hai thuật toán chạy trên cùng một tập tọa độ $(x, y)$ giúp loại bỏ hoàn toàn yếu tố may mắn.

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
*Dữ liệu được đo đạc trung bình trên 5 điểm xuất phát ngẫu nhiên.*

| Thuật toán | N | Tgian TB (ms) | Trạng thái (Ngẫu nhiên) | Phân tích hiện tượng |
| :--- | :--- | :--- | :--- | :--- |
| **Optimized** | 4 | 1.70 | Có ca vô nghiệm | Do định lý đồ thị 4x4 không có đường đi tuần. Nghịch lý Overhead: Trên không gian mẫu quá nhỏ, thuật toán tối ưu chạy chậm ngang Brute-force do tốn chi phí tính toán Heuristic. |
| **Basic** | 4 | 1.92 | Có ca vô nghiệm | Như trên. Quét toàn bộ không gian để kết luận vô nghiệm. |
| **Optimized** | 5 | 926.85 | Có ca vô nghiệm | Hiện tượng lệch chẵn lẻ: Bàn cờ 5x5 có 13 ô Đen, 12 ô Trắng. Nếu xuất phát ngẫu nhiên vào ô Trắng, đồ thị vô nghiệm. Thuật toán phải quét toàn bộ trạng thái để chứng minh điều này. |
| **Basic** | 5 | 2367.84| Có ca vô nghiệm | Quét toàn bộ không gian nhưng chậm hơn do đâm vào các nhánh sâu sai lệch. |
| **Optimized** | 6 | 2.87 | **Thành công** | Đồ thị 6x6 đạt cân bằng chẵn lẻ, luôn có nghiệm. Warnsdorff đi một mạch tới đích không cần quay lui. |
| **Basic** | 6 | Bỏ qua | Quá chậm (>10000ms) | Bùng nổ tổ hợp (Combinatorial Explosion). Không khả thi với Brute-force. |
| **Optimized** | 8 | 11.43 | **Thành công** | Warnsdorff vẫn giải quyết mượt mà trên bàn cờ tiêu chuẩn 8x8. |
| **Basic** | 8 | Bỏ qua | Quá chậm (>10000ms) | Bùng nổ tổ hợp (Combinatorial Explosion). Không khả thi với Brute-force. |
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

| Thuật toán | N | Số lượng nghiệm tìm được | Tổng Tgian (ms) | Nhận xét |
| :--- | :--- | :--- | :--- | :--- |
| **Optimized (Bitmask)**| 3 | **8** | 0.2391 | Quét sạch không gian $9!$, áp dụng Branch & Bound thành công để tìm ra toàn bộ tập nghiệm hoàn chỉnh. |
| **Basic (Siamese)** | 3 | **1** | 0.0102 | Nhanh hơn gấp 20 lần do dùng công thức toán học nội suy, nhưng bỏ sót 7 nghiệm còn lại. |
| **Optimized (Bitmask)**| 4 | N/A | Treo máy (>10000ms) | Không gian tổ hợp bùng nổ lên $16!$ (~20.9 nghìn tỷ hoán vị). Thuật toán Nhánh cận sụp đổ. |
| **Basic (Siamese)** | 4 | 0 | 0.0013 | Phát hiện N chẵn và báo lỗi vô nghiệm theo đúng lý thuyết phương pháp Xiêm. |

---

## Tổng kết Kỹ thuật
Qua thực nghiệm hai hệ thống thuật toán, ta thấy rõ sự đánh đổi (Trade-off) cốt lõi trong phân tích độ phức tạp:
1.  **Về Không gian trạng thái:** Khi đồ thị đạt mức phức tạp nhất định (từ $6 \times 6$ của Mã đi tuần hoặc $4 \times 4$ của Ma phương đếm nghiệm), Backtracking thuần túy (Brute-force) sẽ sụp đổ hoàn toàn do bùng nổ tổ hợp.
2.  **Về Tối ưu hóa:** Việc tích hợp Heuristic (Warnsdorff) hoặc Cắt tỉa (Branch & Bound) là điều kiện bắt buộc để đưa Backtracking vào thực tiễn. Tuy nhiên, các kỹ thuật này mang theo một lượng **Overhead Cost** nhất định, khiến chúng có thể chạy chậm hơn cả Brute-force trên các không gian dữ liệu cực nhỏ (ví dụ: Knight Tour $N=4$).