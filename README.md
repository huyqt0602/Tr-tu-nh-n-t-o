Mô Phỏng Robot Hút Bụi
Dự án mô phỏng hoạt động của robot hút bụi tự động trên môi trường lưới 2D, ứng dụng các thuật toán tìm kiếm trong Trí tuệ nhân tạo để điều hướng và làm sạch môi trường. Giao diện đồ họa được xây dựng bằng Tkinter.

Mục Lục

Giới thiệu
Tính năng
Cấu trúc dự án
Các thuật toán
Cài đặt và chạy
Cách sử dụng
Công nghệ sử dụng


Giới Thiệu
Dự án mô phỏng một robot hút bụi tự động hoạt động trong môi trường lưới ô vuông. Robot thực hiện các bước sau:

Quét môi trường để phát hiện các ô bẩn
Sử dụng thuật toán tìm kiếm để tính đường đi đến ô bẩn gần nhất
Di chuyển đến ô đó và làm sạch
Lặp lại cho đến khi toàn bộ lưới được làm sạch

Đây là bài tập thuộc môn Trí tuệ nhân tạo, minh họa các thuật toán tìm kiếm không có thông tin (uninformed search) và có thông tin (informed search) trên môi trường lưới 2D.

Tính Năng

Môi trường lưới 2D hỗ trợ ô trống, ô bẩn và vật cản
Agent robot tự động xác định và di chuyển đến ô bẩn gần nhất
Hỗ trợ 6 thuật toán tìm kiếm: BFS, DFS, UCS, IDS, Greedy, A*
Giao diện đồ họa trực quan hiển thị quá trình mô phỏng theo từng bước


Cấu Trúc Dự Án
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

Các Thuật Toán
Thuật toánLoạiTối ưuHeuristicMô tảBFSKhông có thông tinCó (số bước)KhôngDuyệt theo chiều rộng, đảm bảo đường đi ngắn nhất tính theo số bướcDFSKhông có thông tinKhôngKhôngDuyệt theo chiều sâu, tiết kiệm bộ nhớ nhưng không đảm bảo tối ưuUCSKhông có thông tinCó (chi phí)KhôngƯu tiên mở rộng nút có tổng chi phí tích lũy nhỏ nhấtIDSKhông có thông tinCó (số bước)KhôngKết hợp ưu điểm của BFS và DFS bằng cách tăng dần giới hạn độ sâuGreedyCó thông tinKhôngManhattanLuôn mở rộng nút có giá trị heuristic nhỏ nhấtA*Có thông tinCóManhattanKết hợp chi phí thực và heuristic, vừa tối ưu vừa hiệu quả
Heuristic sử dụng: Khoảng cách Manhattan — |Δrow| + |Δcol|

Biểu Diễn Môi Trường
Giá trịÝ nghĩa0Ô trống (đã sạch)1Ô bẩn (cần làm sạch)-1Vật cản (không thể đi qua)

Cài Đặt và Chạy
Yêu cầu: Python 3.8 trở lên. Thư viện tkinter đã được tích hợp sẵn trong Python tiêu chuẩn.
bash# Clone repository
git clone https://github.com/huyqt0602/Tr-tu-nh-n-t-o.git
cd Tr-tu-nh-n-t-o/vacuum_cleaner

# Chạy chương trình
python main.py
Nếu hệ thống báo thiếu tkinter:
bash# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

Cách Sử Dụng

Chạy chương trình bằng lệnh python main.py
Chọn thuật toán tìm kiếm từ giao diện (BFS, DFS, UCS, IDS, Greedy, A*)
Thiết lập lưới: xác định vị trí xuất phát của robot, các ô bẩn và vật cản
Nhấn Start để bắt đầu mô phỏng
Quan sát robot di chuyển và làm sạch lần lượt từng ô theo đường đi đã tính


Công Nghệ Sử Dụng

Ngôn ngữ: Python 3
Giao diện: Tkinter
Cấu trúc dữ liệu: Queue, Stack, Heap (heapq), Set
Kiến trúc: Hướng đối tượng (OOP), tách biệt các thành phần Agent, Environment, Algorithm và UI


Tác Giả
huyqt0602 — github.com/huyqt0602
