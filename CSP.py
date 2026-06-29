import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy
import math

BG_DARK       = "#0f0f1a"
BG_CARD       = "#1a1a2e"
BG_CARD_ALT   = "#16213e"
ACCENT_BLUE   = "#0f3460"
ACCENT_CYAN   = "#00d2ff"
ACCENT_PURPLE = "#7b2ff7"
ACCENT_PINK   = "#e94560"
ACCENT_GREEN  = "#00e676"
ACCENT_ORANGE = "#ff9100"
TEXT_PRIMARY   = "#e0e0e0"
TEXT_SECONDARY = "#9e9e9e"
TEXT_BRIGHT    = "#ffffff"

# =====================================================================
# THUẬT TOÁN CSP & MÔ PHỎNG BÀI TOÁN TÔ MÀU BÀN ĐỒ (MAP COLORING)
# =====================================================================

class StepRecordCSP:
    """Lưu lại trạng thái của mỗi bước trong thuật toán CSP."""
    def __init__(self, assignment, domains, current_var, description, status):
        self.assignment = assignment      # dict: var_idx -> màu ('red', 'green', 'yellow')
        self.domains = domains            # dict: var_idx -> list màu còn lại
        self.current_var = current_var    # Tỉnh hiện tại đang xét
        self.description = description    # Mô tả chi tiết bằng tiếng Việt
        self.status = status              # 'init', 'assign', 'forward_checking', 'backtrack', 'success'

def ccw(A, B, C):
    """Kiểm tra xem 3 điểm A, B, C có ngược chiều kim đồng hồ hay không."""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(A, B, C, D):
    """Kiểm tra xem đoạn thẳng AB và CD có cắt nhau hay không (loại trừ trường hợp chung đỉnh)."""
    if A == C or A == D or B == C or B == D:
        return False
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def solve_csp_check(graph, variables, domains, assignment):
    """Hàm giải nhanh CSP để kiểm tra xem đồ thị có giải được bằng 3 màu hay không."""
    if len(assignment) == len(variables):
        return True
    
    # MRV heuristic
    unassigned = [v for v in variables if v not in assignment]
    curr_var = min(unassigned, key=lambda v: (len(domains[v]), -len(graph[v])))
    
    for color in domains[curr_var]:
        conflict = False
        temp_domains = copy.deepcopy(domains)
        for neighbor in graph[curr_var]:
            if neighbor not in assignment:
                if color in temp_domains[neighbor]:
                    temp_domains[neighbor].remove(color)
                    if len(temp_domains[neighbor]) == 0:
                        conflict = True
                        break
        if not conflict:
            assignment[curr_var] = color
            if solve_csp_check(graph, variables, temp_domains, assignment):
                return True
            del assignment[curr_var]
            
    return False

def generate_planar_graph():
    """Tự sinh đồ thị phẳng liên thông từ 6-10 đỉnh không giao nhau và có 3-colorability."""
    while True:
        n = random.randint(6, 10)
        cx, cy = 270, 210
        
        # Chia vòng tròn thành n phần để phân bổ góc
        angles = []
        for i in range(n):
            a_min = i * (2 * math.pi / n)
            a_max = (i + 1) * (2 * math.pi / n)
            angles.append(random.uniform(a_min, a_max))
            
        coords = []
        for a in angles:
            r = random.uniform(110, 160)
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            coords.append((x, y))
            
        # Nối vòng tròn (outer boundary) để đảm bảo liên thông và phẳng
        edges = set()
        for i in range(n):
            u, v = i, (i + 1) % n
            edges.add(tuple(sorted((u, v))))
            
        # Thêm ngẫu nhiên một số dây cung (chords) không giao nhau
        chords_to_add = random.randint(1, 4)
        attempts = 0
        chords_added = 0
        while chords_added < chords_to_add and attempts < 150:
            attempts += 1
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            
            if u == v or abs(u - v) <= 1 or (u == 0 and v == n - 1) or (u == n - 1 and v == 0):
                continue
                
            edge = tuple(sorted((u, v)))
            if edge in edges:
                continue
                
            # Kiểm tra xem dây cung mới có cắt các cạnh hiện có hay không
            crossed = False
            pA, pB = coords[u], coords[v]
            for existing_edge in edges:
                pC, pD = coords[existing_edge[0]], coords[existing_edge[1]]
                if intersect(pA, pB, pC, pD):
                    crossed = True
                    break
                    
            if not crossed:
                edges.add(edge)
                chords_added += 1
                
        # Dựng danh sách kề
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            
        # Xác minh đồ thị có thể tô được bằng 3 màu
        variables = list(range(n))
        domains = {i: ['red', 'green', 'yellow'] for i in range(n)}
        if solve_csp_check(adj, variables, domains, {}):
            return n, coords, adj

def solve_steps_csp(graph, coords):
    """Giải bài toán CSP từng bước và trả về danh sách StepRecordCSP."""
    n = len(coords)
    variables = list(range(n))
    domains = {i: ['red', 'green', 'yellow'] for i in range(n)}
    assignment = {}
    steps = []
    
    # Bước khởi tạo
    steps.append(StepRecordCSP(
        assignment={},
        domains=copy.deepcopy(domains),
        current_var=None,
        description="Khởi tạo: Tất cả các tỉnh đều chưa được tô màu. Miền giá trị ban đầu của mỗi tỉnh là {Đỏ, Xanh, Vàng}.",
        status="init"
    ))
    
    _backtrack_log(graph, variables, domains, assignment, steps)
    return steps

def _backtrack_log(graph, variables, domains, assignment, steps):
    if len(assignment) == len(variables):
        steps.append(StepRecordCSP(
            assignment=copy.deepcopy(assignment),
            domains=copy.deepcopy(domains),
            current_var=None,
            description="✅ ĐÃ HOÀN THÀNH: Tất cả các tỉnh đã được tô màu hợp lệ và không có mâu thuẫn kề!",
            status="success"
        ))
        return True
        
    # Heuristic MRV: chọn biến có miền giá trị nhỏ nhất, tie-breaker là bậc cao nhất
    unassigned = [v for v in variables if v not in assignment]
    curr_var = min(unassigned, key=lambda v: (len(domains[v]), -len(graph[v])))
    curr_name = chr(65 + curr_var)
    
    for color in domains[curr_var]:
        color_vn = COLOR_NAMES_VN[color]
        
        temp_assignment = copy.deepcopy(assignment)
        temp_assignment[curr_var] = color
        
        # Bước gán thử
        steps.append(StepRecordCSP(
            assignment=copy.deepcopy(temp_assignment),
            domains=copy.deepcopy(domains),
            current_var=curr_var,
            description=f"👉 Thử gán màu {color_vn} cho tỉnh {curr_name}.",
            status="assign"
        ))
        
        # Forward Checking
        temp_domains = copy.deepcopy(domains)
        temp_domains[curr_var] = [color]
        
        conflict = False
        fc_logs = []
        
        for neighbor in graph[curr_var]:
            neigh_name = chr(65 + neighbor)
            if neighbor not in temp_assignment:
                if color in temp_domains[neighbor]:
                    temp_domains[neighbor].remove(color)
                    fc_logs.append(f"loại {color_vn} khỏi miền {neigh_name}")
                    if len(temp_domains[neighbor]) == 0:
                        conflict = True
                        fc_logs.append(f"⚠️ miền {neigh_name} rỗng (mâu thuẫn!)")
                        
        if fc_logs:
            desc_fc = f"🔍 Forward Checking từ {curr_name}: {', '.join(fc_logs)}."
        else:
            desc_fc = f"🔍 Forward Checking từ {curr_name}: Không ảnh hưởng các tỉnh kề."
            
        steps.append(StepRecordCSP(
            assignment=copy.deepcopy(temp_assignment),
            domains=copy.deepcopy(temp_domains),
            current_var=curr_var,
            description=desc_fc,
            status="forward_checking"
        ))
        
        if not conflict:
            if _backtrack_log(graph, variables, temp_domains, temp_assignment, steps):
                return True
        else:
            # Ghi bước quay lui
            steps.append(StepRecordCSP(
                assignment=copy.deepcopy(assignment),
                domains=copy.deepcopy(domains),
                current_var=curr_var,
                description=f"❌ Thất bại: Rút lại màu {color_vn} của tỉnh {curr_name} do mâu thuẫn (quay lui).",
                status="backtrack"
            ))
            
    # Hết màu mà vẫn thất bại
    steps.append(StepRecordCSP(
        assignment=copy.deepcopy(assignment),
        domains=copy.deepcopy(domains),
        current_var=None,
        description=f"⏮️ Tất cả các màu thử cho tỉnh {curr_name} đều không hợp lệ. Quay lui về biến trước.",
        status="backtrack"
    ))
    return False

COLOR_MAP = {
    'red': '#ff5252',
    'green': '#00e676',
    'yellow': '#ffd740'
}

COLOR_NAMES_VN = {
    'red': 'Đỏ',
    'green': 'Xanh',
    'yellow': 'Vàng'
}

class CSPMapColoringApp:
    def __init__(self, root, top_root=None):
        self.root = root
        self.top_root = top_root if top_root else root
        self.root.configure(bg=BG_DARK)
        
        self.n = 0
        self.coords = []
        self.graph = {}
        self.steps = []
        self.current_step_idx = -1
        
        self.is_playing = False
        self.play_job = None
        self.play_speed = tk.IntVar(value=1000)
        
        self._build_ui()
        self._on_random_map()
        
    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        left_pane = tk.Frame(self.root, bg=BG_DARK, padx=10, pady=10)
        left_pane.grid(row=0, column=0, sticky="nsew")
        
        right_pane = tk.Frame(self.root, bg=BG_DARK, padx=10, pady=10)
        right_pane.grid(row=0, column=1, sticky="nsew")
        
        # --- Left Pane Content ---
        # Title
        header_frame = tk.Frame(left_pane, bg=BG_DARK)
        header_frame.pack(fill=tk.X, pady=(0, 6))
        
        title_lbl = tk.Label(header_frame, text="🗺️  Mô phỏng CSP Tô màu bản đồ", 
                             font=("Segoe UI", 16, "bold"), fg=ACCENT_CYAN, bg=BG_DARK)
        title_lbl.pack(anchor="w")
        
        # Info Box (Step description)
        info_frame = tk.Frame(left_pane, bg=BG_CARD_ALT, padx=12, pady=10, highlightthickness=1, highlightbackground="#333355")
        info_frame.pack(fill=tk.X, pady=(0, 6))
        
        self.step_label = tk.Label(info_frame, text="Bước: —", font=("Segoe UI", 13, "bold"), fg=ACCENT_ORANGE, bg=BG_CARD_ALT)
        self.step_label.pack(anchor="w")
        
        self.desc_label = tk.Label(info_frame, text="Nhấn '⚡ Giải CSP' để bắt đầu giải từng bước.", font=("Segoe UI", 11), fg=TEXT_PRIMARY, bg=BG_CARD_ALT, justify=tk.LEFT, wraplength=520)
        self.desc_label.pack(anchor="w", pady=(4, 0))
        
        # Canvas
        self.canvas_width = 540
        self.canvas_height = 420
        self.canvas = tk.Canvas(left_pane, width=self.canvas_width, height=self.canvas_height, bg=BG_CARD, highlightthickness=2, highlightbackground=ACCENT_BLUE)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=4)
        
        # Controls Bar
        ctrl_frame = tk.Frame(left_pane, bg=BG_CARD, pady=8, padx=10)
        ctrl_frame.pack(fill=tk.X, pady=(6, 0))
        
        btn_style = {
            "font": ("Segoe UI", 11, "bold"),
            "bd": 0,
            "padx": 12,
            "pady": 6,
            "cursor": "hand2",
            "activeforeground": TEXT_BRIGHT
        }
        
        self.btn_random = tk.Button(ctrl_frame, text="🎲 Bản đồ mới", bg=ACCENT_PURPLE, fg=TEXT_BRIGHT, activebackground="#9c4dff", command=self._on_random_map, **btn_style)
        self.btn_random.pack(side=tk.LEFT, padx=4)
        
        self.btn_solve = tk.Button(ctrl_frame, text="⚡ Giải CSP", bg=ACCENT_GREEN, fg="#1a1a2e", activebackground="#69f0ae", command=self._on_solve, **btn_style)
        self.btn_solve.pack(side=tk.LEFT, padx=4)
        
        self.btn_prev = tk.Button(ctrl_frame, text="◀ Trước", bg="#37474f", fg=TEXT_BRIGHT, activebackground="#546e7a", command=self._on_prev, state=tk.DISABLED, **btn_style)
        self.btn_prev.pack(side=tk.LEFT, padx=4)
        
        self.btn_next = tk.Button(ctrl_frame, text="Tiếp ▶", bg=ACCENT_BLUE, fg=TEXT_BRIGHT, activebackground="#1a4a8a", command=self._on_next, state=tk.DISABLED, **btn_style)
        self.btn_next.pack(side=tk.LEFT, padx=4)
        
        self.btn_play = tk.Button(ctrl_frame, text="▶ Tự động", bg=ACCENT_BLUE, fg=TEXT_BRIGHT, activebackground="#1a4a8a", command=self._toggle_play, **btn_style)
        self.btn_play.pack(side=tk.LEFT, padx=4)
        
        # Speed slider
        speed_frame = tk.Frame(ctrl_frame, bg=BG_CARD)
        speed_frame.pack(side=tk.RIGHT, padx=6)
        tk.Label(speed_frame, text="Tốc độ:", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD).pack(side=tk.LEFT, padx=(0, 4))
        
        speed_slider = tk.Scale(speed_frame, from_=200, to=3000, resolution=100, orient=tk.HORIZONTAL, variable=self.play_speed, bg=BG_CARD, fg=TEXT_PRIMARY, highlightthickness=0, length=90, showvalue=False)
        speed_slider.pack(side=tk.LEFT)
        
        # --- Right Pane Content ---
        # 1. Variables status table (card)
        table_card = tk.Frame(right_pane, bg=BG_CARD, padx=12, pady=10, highlightthickness=1, highlightbackground="#333355")
        table_card.pack(fill=tk.X, pady=(0, 10))
        
        table_title = tk.Label(table_card, text="📋  MIỀN GIÁ TRỊ CÁC BIẾN", font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        table_title.pack(anchor="w", pady=(0, 6))
        
        self.var_table_frame = tk.Frame(table_card, bg=BG_CARD_ALT, padx=6, pady=6)
        self.var_table_frame.pack(fill=tk.X)
        
        # 2. History steps list (card)
        history_card = tk.Frame(right_pane, bg=BG_CARD, padx=12, pady=10, highlightthickness=1, highlightbackground="#333355")
        history_card.pack(fill=tk.BOTH, expand=True)
        
        history_title = tk.Label(history_card, text="📜  LỊCH SỬ BƯỚC ĐI", font=("Segoe UI", 12, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        history_title.pack(anchor="w", pady=(0, 6))
        
        # Listbox & Scrollbar container
        list_container = tk.Frame(history_card, bg=BG_CARD)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        y_scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL)
        x_scrollbar = tk.Scrollbar(list_container, orient=tk.HORIZONTAL)
        
        self.history_listbox = tk.Listbox(list_container, bg=BG_DARK, fg=TEXT_PRIMARY, 
                                          selectbackground=ACCENT_BLUE, selectforeground=TEXT_BRIGHT, 
                                          font=("Segoe UI", 9), bd=0, highlightthickness=0,
                                          xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        
        y_scrollbar.config(command=self.history_listbox.yview)
        x_scrollbar.config(command=self.history_listbox.xview)
        
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.history_listbox.bind("<<ListboxSelect>>", self._on_listbox_select)

    def _on_random_map(self):
        # Tạm dừng nếu đang chạy tự động
        if self.is_playing:
            self._toggle_play()
            
        # Sinh đồ thị phẳng ngẫu nhiên mới
        self.n, self.coords, self.graph = generate_planar_graph()
        self.steps = []
        self.current_step_idx = -1
        
        # Khởi tạo hiển thị bước đầu tiên
        initial_domains = {i: ['red', 'green', 'yellow'] for i in range(self.n)}
        dummy_step = StepRecordCSP({}, initial_domains, None, "Đã tạo bản đồ ngẫu nhiên mới. Nhấn 'Giải CSP' để chạy thuật toán.", "init")
        
        self.step_label.config(text="Bước: — (chưa giải)")
        self.desc_label.config(text=dummy_step.description)
        
        self._draw_map(dummy_step)
        self._update_var_table(dummy_step)
        
        self.history_listbox.delete(0, tk.END)
        self.history_listbox.insert(tk.END, "0. Nhấn 'Giải CSP' để bắt đầu...")
        
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        self.btn_solve.config(state=tk.NORMAL)
        
    def _on_solve(self):
        self.top_root.config(cursor="wait")
        self.top_root.update()
        
        try:
            self.steps = solve_steps_csp(self.graph, self.coords)
            self.current_step_idx = 0
            
            # Populate history listbox
            self.history_listbox.delete(0, tk.END)
            for idx, step in enumerate(self.steps):
                self.history_listbox.insert(tk.END, f"{idx:02d}. {step.description}")
                
            self._display_step(0)
            self.btn_solve.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi giải CSP: {e}")
        finally:
            self.top_root.config(cursor="")
            
    def _display_step(self, idx):
        if idx < 0 or idx >= len(self.steps):
            return
            
        self.current_step_idx = idx
        step = self.steps[idx]
        
        self.step_label.config(text=f"Bước: {idx} / {len(self.steps) - 1}")
        self.desc_label.config(text=step.description)
        
        self._draw_map(step)
        self._update_var_table(step)
        
        # Highlight trong listbox
        self.history_listbox.selection_clear(0, tk.END)
        self.history_listbox.selection_set(idx)
        self.history_listbox.see(idx)
        
        # Cập nhật trạng thái nút bấm
        self.btn_prev.config(state=tk.NORMAL if idx > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if idx < len(self.steps) - 1 else tk.DISABLED)
        
    def _on_prev(self):
        if self.current_step_idx > 0:
            self._display_step(self.current_step_idx - 1)
            
    def _on_next(self):
        if self.current_step_idx < len(self.steps) - 1:
            self._display_step(self.current_step_idx + 1)
            
    def _toggle_play(self):
        if self.is_playing:
            self.is_playing = False
            self.btn_play.config(text="▶ Tự động", bg=ACCENT_BLUE)
            if self.play_job:
                self.root.after_cancel(self.play_job)
                self.play_job = None
        else:
            if not self.steps:
                self._on_solve()
            if not self.steps:
                return
            if self.current_step_idx >= len(self.steps) - 1:
                self._display_step(0)
                
            self.is_playing = True
            self.btn_play.config(text="⏸ Tạm dừng", bg="#e94560")
            self._play_next()
            
    def _play_next(self):
        if not self.is_playing:
            return
        if self.current_step_idx < len(self.steps) - 1:
            self._on_next()
            speed = self.play_speed.get()
            self.play_job = self.root.after(speed, self._play_next)
        else:
            self.is_playing = False
            self.btn_play.config(text="▶ Tự động", bg=ACCENT_BLUE)
            self.play_job = None
            
    def _on_listbox_select(self, event):
        sel = self.history_listbox.curselection()
        if sel:
            idx = sel[0]
            # Tạm dừng chạy tự động nếu người dùng click chọn trực tiếp
            if self.is_playing:
                self._toggle_play()
            self._display_step(idx)

    def _draw_map(self, step):
        self.canvas.delete("all")
        
        # 1. Vẽ các cạnh (đường nối giữa các tỉnh)
        edges = set()
        for u in self.graph:
            for v in self.graph[u]:
                edges.add(tuple(sorted((u, v))))
                
        for u, v in edges:
            x1, y1 = self.coords[u]
            x2, y2 = self.coords[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="#444466", width=2)
            
        # 2. Vẽ các đỉnh (tỉnh thành)
        for i in range(self.n):
            x, y = self.coords[i]
            name = chr(65 + i)
            assigned = step.assignment.get(i, None)
            
            # Vẽ vòng hào quang xung quanh biến đang xét
            if step.current_var == i:
                self.canvas.create_oval(x-28, y-28, x+28, y+28, outline=ACCENT_CYAN, width=3)
                
            # Thân đỉnh (tròn)
            node_fill = COLOR_MAP[assigned] if assigned else BG_CARD_ALT
            node_outline = "#ffffff" if step.current_var == i else (ACCENT_BLUE if assigned else "#444466")
            self.canvas.create_oval(x-22, y-22, x+22, y+22, fill=node_fill, outline=node_outline, width=2)
            
            # Tên đỉnh
            text_color = "#1a1a2e" if assigned else TEXT_PRIMARY
            self.canvas.create_text(x, y, text=name, font=("Segoe UI", 12, "bold"), fill=text_color)
            
            # 3. Vẽ miền giá trị còn lại (dưới dạng 3 chấm màu nhỏ dưới tỉnh)
            domain = step.domains[i]
            # Khoảng cách chấm dưới tỉnh
            dot_y = y + 29
            # Chấm 1: Đỏ
            r_fill = COLOR_MAP['red'] if 'red' in domain else "#1a1a2e"
            r_outline = COLOR_MAP['red'] if 'red' in domain else "#444466"
            self.canvas.create_oval(x-14, dot_y-4, x-6, dot_y+4, fill=r_fill, outline=r_outline, width=1)
            
            # Chấm 2: Xanh
            g_fill = COLOR_MAP['green'] if 'green' in domain else "#1a1a2e"
            g_outline = COLOR_MAP['green'] if 'green' in domain else "#444466"
            self.canvas.create_oval(x-4, dot_y-4, x+4, dot_y+4, fill=g_fill, outline=g_outline, width=1)
            
            # Chấm 3: Vàng
            y_fill = COLOR_MAP['yellow'] if 'yellow' in domain else "#1a1a2e"
            y_outline = COLOR_MAP['yellow'] if 'yellow' in domain else "#444466"
            self.canvas.create_oval(x+6, dot_y-4, x+14, dot_y+4, fill=y_fill, outline=y_outline, width=1)

    def _update_var_table(self, step):
        # Xóa các dòng cũ
        for widget in self.var_table_frame.winfo_children():
            widget.destroy()
            
        # Vẽ Header của bảng miền giá trị
        tk.Label(self.var_table_frame, text="Tỉnh", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_CARD_ALT, width=6, anchor="w").grid(row=0, column=0, padx=4, pady=2)
        tk.Label(self.var_table_frame, text="Màu đã tô", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_CARD_ALT, width=10, anchor="w").grid(row=0, column=1, padx=4, pady=2)
        tk.Label(self.var_table_frame, text="Miền giá trị", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_CARD_ALT, width=18, anchor="w").grid(row=0, column=2, padx=4, pady=2)
        
        # Điền thông tin từng tỉnh thành
        for i in range(self.n):
            name = chr(65 + i)
            assigned = step.assignment.get(i, None)
            assigned_text = COLOR_NAMES_VN[assigned] if assigned else "—"
            assigned_color = COLOR_MAP[assigned] if assigned else TEXT_SECONDARY
            
            domain = step.domains[i]
            domain_text = ", ".join([COLOR_NAMES_VN[c] for c in domain])
            if not domain:
                domain_text = "⚠️ Rỗng"
                
            is_curr = (step.current_var == i)
            row_bg = "#1f3154" if is_curr else BG_CARD_ALT
            row_fg = TEXT_BRIGHT if is_curr else TEXT_PRIMARY
            
            lbl_name = tk.Label(self.var_table_frame, text=name, font=("Segoe UI", 9, "bold" if is_curr else "normal"), fg=ACCENT_ORANGE if is_curr else row_fg, bg=row_bg, width=6, anchor="w")
            lbl_name.grid(row=i+1, column=0, padx=4, pady=1)
            
            lbl_color = tk.Label(self.var_table_frame, text=assigned_text, font=("Segoe UI", 9, "bold" if assigned else "normal"), fg=assigned_color, bg=row_bg, width=10, anchor="w")
            lbl_color.grid(row=i+1, column=1, padx=4, pady=1)
            
            lbl_domain = tk.Label(self.var_table_frame, text=domain_text, font=("Segoe UI", 9), fg="#ff5252" if not domain else row_fg, bg=row_bg, width=18, anchor="w")
            lbl_domain.grid(row=i+1, column=2, padx=4, pady=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Trình Mô Phỏng CSP - Tô Màu Bản Đồ (Map Coloring)")
    win_w, win_h = 1100, 700
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - win_w) // 2
    y = (sh - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")
    root.resizable(True, True)

    app = CSPMapColoringApp(root)
    root.mainloop()