# Mô Phỏng Robot Hút Bụi

Dự án mô phỏng hoạt động của robot hút bụi tự động trên môi trường lưới 2D, ứng dụng các thuật toán tìm kiếm trong Trí tuệ nhân tạo để điều hướng và làm sạch môi trường. Giao diện đồ họa được xây dựng bằng **Tkinter**.

---

## Mục Lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Các thuật toán](#các-thuật-toán)
- [Cài đặt và chạy](#cài-đặt-và-chạy)
- [Cách sử dụng](#cách-sử-dụng)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)

---

## Giới Thiệu

Dự án mô phỏng một robot hút bụi tự động hoạt động trong môi trường lưới ô vuông. Robot thực hiện các bước sau:

1. Quét môi trường để phát hiện các ô bẩn
2. Sử dụng thuật toán tìm kiếm để tính đường đi đến ô bẩn gần nhất
3. Di chuyển đến ô đó và làm sạch
4. Lặp lại cho đến khi toàn bộ lưới được làm sạch

Đây là bài tập thuộc môn **Trí tuệ nhân tạo**, minh họa các thuật toán tìm kiếm không có thông tin (uninformed search), có thông tin (informed search) và tìm kiếm cục bộ (local search) trên môi trường lưới 2D.

---

## Tính Năng

- Môi trường lưới 2D hỗ trợ ô trống, ô bẩn và vật cản
- Agent robot tự động xác định và di chuyển đến ô bẩn gần nhất
- Hỗ trợ 10 thuật toán tìm kiếm thuộc 3 nhóm: Tìm kiếm mù, Tìm kiếm có thông tin, Tìm kiếm cục bộ
- Giao diện đồ họa trực quan hiển thị quá trình mô phỏng theo từng bước

---

## Cấu Trúc Dự Án

```
vacuum_cleaner/
│
├── main.py                           # Điểm khởi chạy chương trình
│
├── agents/
│   └── vacuum_agent.py               # Logic điều khiển robot hút bụi
│
├── environment/
│   └── grid_environment.py           # Quản lý môi trường lưới 2D
│
├── algorithms/
│   ├── base_algorithm.py             # Lớp trừu tượng (Abstract Base Class)
│   │
│   │   -- Tìm kiếm không có thông tin --
│   ├── bfs_algorithm.py              # Tìm kiếm theo chiều rộng (BFS)
│   ├── dfs_algorithm.py              # Tìm kiếm theo chiều sâu (DFS)
│   ├── ucs_algorithm.py              # Tìm kiếm chi phí đồng nhất (UCS)
│   ├── ids_algorithm.py              # Tìm kiếm sâu dần (IDS)
│   │
│   │   -- Tìm kiếm có thông tin --
│   ├── greedy_algorithm.py           # Tìm kiếm tham lam (Greedy)
│   ├── astar_algorithm.py            # Thuật toán A*
│   ├── idastar_algorithm.py          # Thuật toán IDA*
│   │
│   │   -- Tìm kiếm cục bộ (Local Search) --
│   ├── simple_hill_climbing.py       # Leo đồi đơn giản
│   ├── steepest_hill_climbing.py     # Leo đồi dốc nhất
│   ├── stochastic_hill_climbing.py   # Leo đồi ngẫu nhiên
|   └── random_restart_hill_climbing  # Leo đồi khởi tạo ngẫu nhiên
│
└── ui/
    └── vacuum_ui.py                  # Giao diện đồ họa Tkinter
```

---

## Các Thuật Toán

### Nhóm 1 — Tìm kiếm không có thông tin (Uninformed Search)

| Thuật toán | Tối ưu | Mô tả |
|---|---|---|
| BFS | Có (số bước) | Duyệt theo chiều rộng, đảm bảo đường đi ngắn nhất tính theo số bước |
| DFS | Không | Duyệt theo chiều sâu, tiết kiệm bộ nhớ nhưng không đảm bảo tối ưu |
| UCS | Có (chi phí) | Ưu tiên mở rộng nút có tổng chi phí tích lũy nhỏ nhất |
| IDS | Có (số bước) | Kết hợp ưu điểm BFS và DFS bằng cách tăng dần giới hạn độ sâu |

### Nhóm 2 — Tìm kiếm có thông tin (Informed Search)

Hàm heuristic sử dụng: khoảng cách Manhattan — `h = |Δrow| + |Δcol|`

| Thuật toán | Tối ưu | Mô tả |
|---|---|---|
| Greedy | Không | Luôn mở rộng nút có giá trị heuristic nhỏ nhất |
| A\* | Có | Kết hợp chi phí thực `g` và heuristic `h`, hàm đánh giá `f = g + h` |
| IDA\* | Có | Phiên bản tiết kiệm bộ nhớ của A\*, dùng ngưỡng `f` thay cho độ sâu trong IDS |

### Nhóm 3 — Tìm kiếm cục bộ (Local Search) 

Hàm giá trị (value): `v = −Manhattan(vị_trí, goal)` — cực đại hóa tương đương tối thiểu hóa khoảng cách.

| Thuật toán | Mô tả |
|---|---|
| Leo đồi đơn giản (Simple HC) | Chuyển sang trạng thái lân cận **đầu tiên** tốt hơn trạng thái hiện tại. Dừng khi đạt cực đại cục bộ. |
| Leo đồi dốc nhất (Steepest HC) | Sinh **tất cả** lân cận, chọn lân cận **tốt nhất**. Dừng nếu lân cận tốt nhất không vượt trội hơn hiện tại. |
| Leo đồi ngẫu nhiên (Stochastic HC) | Lọc ra tập `Better_Neighbors` (tốt hơn hiện tại), chọn **ngẫu nhiên** một trạng thái từ tập đó. Dừng khi tập rỗng. |

> **Lưu ý về Local Search:** Các thuật toán leo đồi không đảm bảo tìm được đích trong mọi trường hợp. Khi bị kẹt ở cực đại cục bộ (do vật cản), robot sẽ hiển thị đường đi đến vị trí tốt nhất đã đạt được.

---

## Biểu Diễn Môi Trường

| Giá trị | Ý nghĩa |
|---|---|
| `0` | Ô trống (đã sạch) |
| `1` | Ô bẩn (cần làm sạch) |
| `-1` | Vật cản (không thể đi qua) |

---

## Cài Đặt và Chạy

**Yêu cầu:** Python 3.8 trở lên. Thư viện `tkinter` đã được tích hợp sẵn trong Python tiêu chuẩn.

```bash
# Clone repository
git clone https://github.com/huyqt0602/Tr-tu-nh-n-t-o.git
cd Tr-tu-nh-n-t-o/vacuum_cleaner

# Chạy chương trình
python main.py
```

Nếu hệ thống báo thiếu `tkinter`:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

---

## Cách Sử Dụng

1. Chạy chương trình bằng lệnh `python main.py`
2. Chọn thuật toán từ thanh bên trái (nhóm Tìm kiếm hoặc Local Search)
3. Nhấn **BẮT ĐẦU** để chạy mô phỏng
4. Quan sát robot di chuyển và làm sạch từng ô; nhật ký hoạt động hiển thị bên phải
5. Nhấn **RESET** để khôi phục lại trạng thái ban đầu

---

## Công Nghệ Sử Dụng

- **Ngôn ngữ:** Python 3
- **Giao diện:** Tkinter
- **Cấu trúc dữ liệu:** Queue, Stack, Heap (`heapq`), Set
- **Kiến trúc:** Hướng đối tượng (OOP), tách biệt các thành phần Agent, Environment, Algorithm và UI

---

## Tác Giả

**huyqt0602** — [github.com/huyqt0602](https://github.com/huyqt0602)
