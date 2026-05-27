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

Đây là bài tập thuộc môn **Trí tuệ nhân tạo**, minh họa các thuật toán tìm kiếm không có thông tin (uninformed search) và có thông tin (informed search) trên môi trường lưới 2D.

---

## Tính Năng

- Môi trường lưới 2D hỗ trợ ô trống, ô bẩn và vật cản
- Agent robot tự động xác định và di chuyển đến ô bẩn gần nhất
- Hỗ trợ 6 thuật toán tìm kiếm: BFS, DFS, UCS, IDS, Greedy, A\*
- Giao diện đồ họa trực quan hiển thị quá trình mô phỏng theo từng bước

---

## Cấu Trúc Dự Án

```
vacuum_cleaner/
│
├── main.py                        # Điểm khởi chạy chương trình
│
├── agents/
│   └── vacuum_agent.py            # Logic điều khiển robot hút bụi
│
├── environment/
│   └── grid_environment.py        # Quản lý môi trường lưới 2D
│
├── algorithms/
│   ├── base_algorithm.py          # Lớp trừu tượng (Abstract Base Class)
│   ├── bfs_algorithm.py           # Tìm kiếm theo chiều rộng (BFS)
│   ├── dfs_algorithm.py           # Tìm kiếm theo chiều sâu (DFS)
│   ├── ucs_algorithm.py           # Tìm kiếm chi phí đồng nhất (UCS)
│   ├── ids_algorithm.py           # Tìm kiếm sâu dần (IDS)
│   ├── greedy_algorithm.py        # Tìm kiếm tham lam (Greedy)
│   └── astar_algorithm.py         # Thuật toán A*
│
└── ui/
    └── vacuum_ui.py               # Giao diện đồ họa Tkinter
```

---

## Các Thuật Toán

| Thuật toán | Loại | Tối ưu | Heuristic | Mô tả |
|---|---|---|---|---|
| BFS | Không có thông tin | Có (số bước) | Không | Duyệt theo chiều rộng, đảm bảo đường đi ngắn nhất tính theo số bước |
| DFS | Không có thông tin | Không | Không | Duyệt theo chiều sâu, tiết kiệm bộ nhớ nhưng không đảm bảo tối ưu |
| UCS | Không có thông tin | Có (chi phí) | Không | Ưu tiên mở rộng nút có tổng chi phí tích lũy nhỏ nhất |
| IDS | Không có thông tin | Có (số bước) | Không | Kết hợp ưu điểm của BFS và DFS bằng cách tăng dần giới hạn độ sâu |
| Greedy | Có thông tin | Không | Manhattan | Luôn mở rộng nút có giá trị heuristic nhỏ nhất |
| A\* | Có thông tin | Có | Manhattan | Kết hợp chi phí thực và heuristic, vừa tối ưu vừa hiệu quả |

**Heuristic sử dụng:** Khoảng cách Manhattan — `|Δrow| + |Δcol|`

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
2. Chọn thuật toán tìm kiếm từ giao diện (BFS, DFS, UCS, IDS, Greedy, A\*)
3. Thiết lập lưới: xác định vị trí xuất phát của robot, các ô bẩn và vật cản
4. Nhấn **Start** để bắt đầu mô phỏng
5. Quan sát robot di chuyển và làm sạch lần lượt từng ô theo đường đi đã tính

---

## Công Nghệ Sử Dụng

- **Ngôn ngữ:** Python 3
- **Giao diện:** Tkinter
- **Cấu trúc dữ liệu:** Queue, Stack, Heap (`heapq`), Set
- **Kiến trúc:** Hướng đối tượng (OOP), tách biệt các thành phần Agent, Environment, Algorithm và UI

---

## Tác Giả

**huyqt0602** — [github.com/huyqt0602](https://github.com/huyqt0602)

