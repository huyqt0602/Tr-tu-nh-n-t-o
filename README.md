# Dự Án Mô Phỏng AI: Robot Hút Bụi & CSP Tô Màu Bản Đồ

Dự án này chứa hai ứng dụng mô phỏng các thuật toán trí tuệ nhân tạo (AI) trực quan bằng giao diện đồ họa **Tkinter** trong Python:
1. **Mô Phỏng Robot Hút Bụi (Vacuum Cleaner Simulation)**: Ứng dụng các thuật toán tìm kiếm đường đi (Uninformed, Informed, Local Search).
2. **Mô Phỏng Tô Màu Bản Đồ CSP (Constraint Satisfaction Problem)**: Giải bài toán tô màu bản đồ bằng thuật toán CSP Backtracking kết hợp Heuristic MRV và kỹ thuật Forward Checking.

---

## Mục Lục

- [Yêu Cầu Hệ Thống & Cài Đặt](#yêu-cầu-hệ-thống--cài-đặt)
- [1. Mô Phỏng Robot Hút Bụi](#1-mô-phỏng-robot-hút-bụi)
  - [Tính năng](#tính-năng)
  - [Cấu trúc thư mục](#cấu-trúc-thư-mục)
  - [Các thuật toán tìm kiếm](#các-thuật-toán-tìm-kiếm)
  - [Cách khởi chạy](#cách-khởi-chạy)
- [2. Mô Phỏng Tô Màu Bản Đồ CSP](#2-mô-phỏng-tô-màu-bản-đồ-csp)
  - [Giới thiệu bài toán](#giới-thiệu-bài-toán)
  - [Tính năng chính](#tính-năng-chính)
  - [Thuật toán áp dụng](#thuật-toán-áp-dụng)
  - [Cách khởi chạy](#cách-khởi-chạy-1)
- [Tác Giả](#tác-giả)

---

## Yêu Cầu Hệ Thống & Cài Đặt

**Yêu cầu:** Python 3.8 trở lên. Thư viện đồ họa `tkinter` đã được tích hợp sẵn trong bộ cài đặt Python tiêu chuẩn trên Windows.

Nếu chạy trên Linux hoặc macOS và bị báo thiếu `tkinter`, cài đặt bằng lệnh tương ứng:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

---

## 1. Mô Phỏng Robot Hút Bụi

Ứng dụng mô phỏng hoạt động của một robot hút bụi tự động hoạt động trên môi trường lưới 2D. Robot quét tìm các ô bẩn, sử dụng thuật toán tìm kiếm để tìm đường đi ngắn nhất đến ô bẩn gần nhất, di chuyển đến và làm sạch nó.

### Tính năng
- Môi trường lưới ô vuông 2D tùy chỉnh ô trống, ô bẩn, vật cản.
- Robot tự động xác định mục tiêu và tìm đường tối ưu nhất để dọn dẹp.
- Giao diện trực quan thể hiện quá trình duyệt node của robot và nhật ký dọn dẹp theo thời gian thực.

### Cấu trúc thư mục
```
vaccum_cleaner/
├── main.py                                # Điểm khởi chạy mô phỏng Robot hút bụi
├── agents/
│   └── vacuum_agent.py                    # Logic điều khiển và di chuyển của robot
├── environment/
│   └── grid_environment.py                # Quản lý bản đồ lưới 2D (bẩn, vật cản, robot)
├── algorithms/
│   ├── base_algorithm.py                  # Lớp cơ sở trừu tượng cho các thuật toán
│   ├── bfs_algorithm.py                   # Tìm kiếm theo chiều rộng (BFS)
│   ├── dfs_algorithm.py                   # Tìm kiếm theo chiều sâu (DFS)
│   ├── ucs_algorithm.py                   # Tìm kiếm chi phí đồng nhất (UCS)
│   ├── ids_algorithm.py                   # Tìm kiếm sâu dần (IDS)
│   ├── greedy_algorithm.py                # Tìm kiếm tham lam (Greedy)
│   ├── astar_algorithm.py                 # Thuật toán A*
│   ├── idastar_algorithm.py               # Thuật toán IDA*
│   ├── simple_hill_climbing.py            # Leo đồi đơn giản (Simple HC)
│   ├── steepest_hill_climbing.py          # Leo đồi dốc nhất (Steepest HC)
│   ├── stochastic_hill_climbing.py        # Leo đồi ngẫu nhiên (Stochastic HC)
│   ├── random_restart_hill_climbing.py    # Leo đồi khởi tạo ngẫu nhiên
│   ├── local_beam_search.py               # Tìm kiếm chùm cục bộ (Local Beam)
│   └── simulated_annealing.py             # Mô phỏng luyện kim (Simulated Annealing)
└── ui/
    └── vacuum_ui.py                       # Giao diện đồ họa Tkinter của Robot hút bụi
```

### Các thuật toán tìm kiếm

| Nhóm thuật toán | Tên thuật toán | Tối ưu | Mô tả |
| :--- | :--- | :--- | :--- |
| **Không có thông tin** | BFS | Có | Tìm đường đi ngắn nhất theo số bước |
| | DFS | Không | Ưu tiên đi sâu, tiết kiệm bộ nhớ |
| | UCS | Có | Ưu tiên mở rộng nút có chi phí tích lũy thấp nhất |
| | IDS | Có | Tăng dần giới hạn độ sâu của DFS |
| **Có thông tin (Heuristic)** | Greedy | Không | Chọn nút có khoảng cách Manhattan ngắn nhất đến đích |
| | A* | Có | Đánh giá hàm số $f(n) = g(n) + h(n)$ |
| | IDA* | Có | Kết hợp ý tưởng giới hạn ngưỡng $f$ và IDS |
| **Tìm kiếm cục bộ** | Simple HC | Không | Chọn trạng thái lân cận tốt hơn đầu tiên |
| | Steepest HC | Không | Chọn trạng thái lân cận tốt nhất trong tất cả |
| | Stochastic HC| Không | Chọn ngẫu nhiên một trạng thái lân cận tốt hơn |
| | Random Restart| Không | Leo đồi nhiều lần từ các điểm xuất phát ngẫu nhiên |
| | Local Beam | Không | Duy trì đồng thời $k$ chùm trạng thái |
| | Simulated Annealing | Không | Chấp nhận nước đi tệ hơn dựa trên nhiệt độ giảm dần |

### Cách khởi chạy
Chạy lệnh sau tại thư mục gốc của dự án:
```bash
python main.py
```

---

## 2. Mô Phỏng Tô Màu Bản Đồ CSP

Ứng dụng giải bài toán **Tô màu bản đồ (Map Coloring)** - một dạng điển hình của bài toán **Thỏa mãn ràng buộc (Constraint Satisfaction Problem - CSP)**. Chương trình cho phép tô màu một đồ thị phẳng ngẫu nhiên (đại diện cho các tỉnh liền kề trên bản đồ) bằng 3 màu (Đỏ, Xanh lá, Vàng) sao cho không có hai tỉnh kề nhau nào trùng màu.

### Giới thiệu bài toán
- **Biến ($X$):** Các tỉnh thành trên bản đồ (đỉnh của đồ thị $A, B, C...$).
- **Miền giá trị ($D$):** $\{\text{Đỏ}, \text{Xanh lá}, \text{Vàng}\}$.
- **Ràng buộc ($C$):** Hai tỉnh có biên giới chung (kề nhau) phải có màu khác nhau.

### Tính năng chính
- **Tự động sinh bản đồ phẳng ngẫu nhiên** liên thông từ 6-10 tỉnh thành không giao nhau về mặt hình học và luôn đảm bảo có lời giải.
- **Trực quan hóa từng bước**:
  - Trạng thái tô màu hiện tại của từng tỉnh.
  - Vòng hào quang highlight tỉnh đang được xét ở bước hiện tại.
  - Bảng hiển thị miền giá trị (domain) còn lại của từng tỉnh.
  - Ba chấm màu nhỏ trực quan hóa miền giá trị ngay dưới mỗi tỉnh trên bản đồ.
- **Lịch sử bước đi chi tiết**: Hiển thị nhật ký hoạt động (thử gán màu, Forward Checking loại màu, Quay lui backtrack khi gặp mâu thuẫn) bằng tiếng Việt.
- **Chế độ điều khiển linh hoạt**: Cho phép xem từng bước bằng nút bấm (Trước/Sau), tự động chạy mô phỏng (Play/Pause) với thanh điều chỉnh tốc độ.

### Thuật toán áp dụng
- **CSP Backtracking**: Thuật toán tìm kiếm quay lui cải tiến cho bài toán thỏa mãn ràng buộc.
- **Heuristic MRV (Minimum Remaining Values)**: Ưu tiên chọn tỉnh có ít màu có thể tô nhất (miền giá trị nhỏ nhất) để xét trước. Trường hợp bằng nhau (tie-breaker), ưu tiên tỉnh có nhiều liên kết kề nhất (độ bậc cao nhất).
- **Forward Checking (Kiểm tra phía trước)**: Mỗi khi tô màu một tỉnh, lập tức loại bỏ màu đó khỏi miền giá trị của các tỉnh kề chưa được tô màu. Nếu miền giá trị của một tỉnh kề trở nên rỗng, thuật toán phát hiện mâu thuẫn sớm và quay lui ngay lập tức mà không cần đi tiếp vào nhánh lỗi.

### Cách khởi chạy
Chạy lệnh sau tại thư mục gốc của dự án:
```bash
python Bt_canhan_AI.py
```

---

## Tác Giả

**huyqt0602** — [github.com/huyqt0602](https://github.com/huyqt0602)
