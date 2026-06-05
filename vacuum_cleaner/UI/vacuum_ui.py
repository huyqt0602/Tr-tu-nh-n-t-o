import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from environment.grid_environment import GridEnvironment

from algorithms.bfs_algorithm import BFSAlgorithm
from algorithms.dfs_algorithm import DFSAlgorithm
from algorithms.ids_algorithm import IDSAlgorithm
from algorithms.ucs_algorithm import UCSAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.astar_algorithm import AStarAlgorithm
from algorithms.idastar_algorithm import IDAStarAlgorithm
from algorithms.simple_hill_climbing import SimpleHillClimbingAlgorithm
from algorithms.steepest_hill_climbing import SteepestHillClimbingAlgorithm
from algorithms.stochastic_hill_climbing import StochasticHillClimbingAlgorithm
from algorithms.random_restart_hill_climbing import RandomRestartHillClimbingAlgorithm
from algorithms.local_beam_search import LocalBeamSearchAlgorithm
from algorithms.simulated_annealing import SimulatedAnnealingAlgorithm

from agents.vacuum_agent import VacuumAgent

# ── BẢNG MÀU ───────────────────────────────────────────
_BG      = "#1e293b"   
_PANEL   = "#0f172a"   
_CARD    = "#334155"   
_BORDER  = "#475569"   
_TEXT    = "#f1f5f9"   
_MUTED   = "#94a3b8"   

_GREEN   = "#10b981"   
_VIOLET  = "#8b5cf6"   
_AMBER   = "#f59e0b"   

_C_EMPTY    = "#1e293b"   
_C_DIRT     = "#b45309"   
_C_VISITED  = "#0f766e"   
_C_OBSTACLE = "#7f1d1d"   
_C_ROBOT    = "#3b82f6"   

_C_X_MARK   = "#fca5a5"   
_C_TEXT_COORD= "#64748b"  


class VacuumUI:

    CELL = 82          
    ANIM = 210         

    _DEFAULT_GRID = [
        [0,  1,  0,  0],
        [1, -1,  1,  0],
        [0,  0,  1,  0],
        [1,  0, -1,  1],
    ]

    _ALGO_MAP = {
        "BFS":               BFSAlgorithm,
        "DFS":               DFSAlgorithm,
        "IDS":               IDSAlgorithm,
        "UCS":               UCSAlgorithm,
        "GREEDY":            GreedyAlgorithm,
        "A*":                AStarAlgorithm,
        "IDA*":              IDAStarAlgorithm,
        "SIMPLE HC":         SimpleHillClimbingAlgorithm,
        "STEEPEST HC":       SteepestHillClimbingAlgorithm,
        "STOCHASTIC HC":     StochasticHillClimbingAlgorithm,
        "RANDOM RESTART HC": RandomRestartHillClimbingAlgorithm,
        "LOCAL BEAM":        LocalBeamSearchAlgorithm,
        "SIMULATED ANNEAL":  SimulatedAnnealingAlgorithm,
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Robot Hút Bụi — AI Algorithms")
        self.root.geometry("1300x820")
        self.root.resizable(False, False)
        self.root.configure(bg=_BG)

        self.original_grid = [row[:] for row in self._DEFAULT_GRID]
        self._reset_state()
        self._build()
        self.draw_grid()

    def _reset_state(self):
        self.environment   = GridEnvironment([r[:] for r in self.original_grid])
        self.robot_pos     = (0, 0)
        self.visited       = []
        self.path          = []
        self._oval_id      = None
        self._robot_lbl_id = None

    def _build(self):
        self._make_topbar()

        body = tk.Frame(self.root, bg=_BG)
        body.pack(fill="both", expand=True, padx=12, pady=(6, 0))

        self._make_sidebar(body)
        self._make_canvas_area(body)
        self._make_log_panel(body)

        self._make_statusbar()

    # ── Top bar ──────────────────────────────────────────────────────────
    def _make_topbar(self):
        bar = tk.Frame(self.root, bg=_PANEL, height=50, bd=1, relief="solid")
        bar.config(highlightbackground=_BORDER, highlightthickness=1)
        bar.pack(fill="x")
        
        tk.Label(bar, text="ROBOT HÚT BỤI AI",
                 bg=_PANEL, fg=_TEXT,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=18, pady=10)
        tk.Label(bar, text="Trí tuệ nhân tạo · Mô phỏng thuật toán tìm kiếm",
                 bg=_PANEL, fg=_MUTED,
                 font=("Segoe UI", 9)).pack(side="left", pady=14)

    # ── Sidebar ──────────────────────────────────────────────────────────
    def _make_sidebar(self, parent):
        sb = tk.Frame(parent, bg=_PANEL, width=235, highlightbackground=_BORDER, highlightthickness=1)
        sb.pack(side="left", fill="y", padx=(0, 10))
        sb.pack_propagate(False)

        self.algo_var = tk.StringVar(value="BFS")

        self._grp_header(sb, "TÌM KIẾM", _GREEN)
        for lbl, val in [
            ("BFS",    "BFS"),
            ("DFS",    "DFS"),
            ("IDS",    "IDS"),
            ("UCS",    "UCS"),
            ("Greedy", "GREEDY"),
            ("A*",     "A*"),
            ("IDA*",   "IDA*"),
        ]:
            self._radio(sb, lbl, val, _GREEN)

        self._grp_header(sb, "LOCAL SEARCH", _VIOLET)
        for lbl, val in [
            ("Leo đồi đơn giản",    "SIMPLE HC"),
            ("Leo đồi dốc nhất",     "STEEPEST HC"),
            ("Leo đồi ngẫu nhiên",   "STOCHASTIC HC"),
            ("Leo đồi khởi tạo ngẫu nhiên",  "RANDOM RESTART HC"),

            ("Tìm kiếm chùm (k=3)",  "LOCAL BEAM"),
            ("Ủ mô phỏng (SA)",      "SIMULATED ANNEAL"),
        ]:
            self._radio(sb, lbl, val, _VIOLET)

        tk.Frame(sb, bg=_PANEL, height=15).pack()
        
        tk.Button(sb, text="▶   BẮT ĐẦU",
                  command=self.start_cleaning,
                  bg=_GREEN, fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2",
                  width=20, pady=7).pack(padx=14, pady=(0, 8))
                  
        tk.Button(sb, text="↺   RESET",
                  command=self.reset_environment,
                  bg="#ef4444", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2",
                  width=20, pady=7).pack(padx=14)

    def _grp_header(self, parent, text, color):
        f = tk.Frame(parent, bg=_PANEL)
        f.pack(fill="x", padx=12, pady=(12, 4))
        tk.Frame(f, bg=color, width=4, height=14).pack(side="left")
        tk.Label(f, text=f"  {text}",
                 bg=_PANEL, fg=color,
                 font=("Segoe UI", 8, "bold")).pack(side="left")

    def _radio(self, parent, text, value, accent):
        tk.Radiobutton(
            parent,
            text=f"  {text}",
            variable=self.algo_var,
            value=value,
            indicatoron=False,
            anchor="w",
            width=22,
            font=("Segoe UI", 9),
            bg=_PANEL, fg=_TEXT,
            selectcolor=_BG,
            activebackground=_CARD,
            activeforeground=_TEXT,
            relief="flat", pady=3,
            cursor="hand2",
            bd=0,
            highlightthickness=0
        ).pack(fill="x", padx=14, pady=1)

    # ── Canvas area ──────────────────────────────────────────────────────
    def _make_canvas_area(self, parent):
        cf = tk.Frame(parent, bg=_BG)
        cf.pack(side="left", fill="both", expand=True)

        leg = tk.Frame(cf, bg=_BG)
        leg.pack(pady=(2, 6))
        for color, label in [
            (_C_DIRT,     "Bụi"),
            (_C_VISITED,  "Đã đi"),
            (_C_OBSTACLE, "Vật cản"),
            (_C_ROBOT,    "Robot"),
            (_C_EMPTY,    "Sạch"),
        ]:
            tk.Frame(leg, bg=color, width=12, height=12, bd=1, relief="solid").pack(side="left", padx=(10, 3))
            tk.Label(leg, text=label, bg=_BG, fg=_TEXT,
                     font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 8))

        gw = self.CELL * 4 + 100
        gh = self.CELL * 4 + 60
        self.canvas = tk.Canvas(
            cf, width=gw, height=gh,
            bg=_CARD,
            highlightthickness=1, highlightbackground=_BORDER,
        )
        self.canvas.pack(pady=2)

    # ── Log panel ────────────────────────────────────────────────────────
    def _make_log_panel(self, parent):
        rp = tk.Frame(parent, bg=_PANEL, width=260, highlightbackground=_BORDER, highlightthickness=1)
        rp.pack(side="right", fill="y", padx=(10, 0))
        rp.pack_propagate(False)

        tk.Label(rp, text="NHẬT KÝ HOẠT ĐỘNG",
                 bg=_PANEL, fg=_TEXT,
                 font=("Segoe UI", 10, "bold")).pack(pady=(12, 6), padx=12, anchor="w")

        self.log_text = ScrolledText(
            rp,
            font=("Consolas", 9),
            bg=_PANEL, fg="#34d399",
            insertbackground=_TEXT,
            relief="flat", borderwidth=0, wrap="word",
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 12))

    # ── Status bar ───────────────────────────────────────────────────────
    def _make_statusbar(self):
        bar = tk.Frame(self.root, bg=_PANEL, height=36, highlightbackground=_BORDER, highlightthickness=1)
        bar.pack(fill="x", side="bottom")

        self.lbl_status = tk.Label(bar, text="● Sẵn sàng",
                                    bg=_PANEL, fg=_GREEN,
                                    font=("Segoe UI", 9, "bold"))
        self.lbl_status.pack(side="left", padx=16, pady=6)

        self.lbl_steps = tk.Label(bar, text="Bước: 0",
                                   bg=_PANEL, fg=_TEXT,
                                   font=("Segoe UI", 9, "bold"))
        self.lbl_steps.pack(side="left", padx=12)

        self.lbl_algo = tk.Label(bar, text="",
                                  bg=_PANEL, fg=_VIOLET,
                                  font=("Segoe UI", 9, "italic", "bold"))
        self.lbl_algo.pack(side="right", padx=16)

    # ══════════════════════════════════════════════════════════════════════
    #  DRAW
    # ══════════════════════════════════════════════════════════════════════
    _PX, _PY = 50, 28

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.environment.rows):
            for c in range(self.environment.cols):
                self._draw_cell(r, c)
        self._draw_robot()

    def _draw_cell(self, r, c):
        x1 = self._PX + c * self.CELL
        y1 = self._PY + r * self.CELL
        x2, y2 = x1 + self.CELL, y1 + self.CELL
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2

        val   = self.environment.grid[r][c]
        color = _C_EMPTY
        if (r, c) in self.visited: color = _C_VISITED
        if val ==  1:              color = _C_DIRT
        if val == -1:              color = _C_OBSTACLE

        self.canvas.create_rectangle(x1, y1, x2, y2,
                                      fill=color, outline=_BORDER, width=2)
        if val == 1:
            self.canvas.create_text(mx, my, text="BỤI",
                                     fill="#fcd34d", font=("Segoe UI", 10, "bold"))
        elif val == -1:
            self.canvas.create_text(mx, my, text="✕",
                                     fill=_C_X_MARK, font=("Segoe UI", 18, "bold"))

        self.canvas.create_text(x1 + 10, y1 + 10, text=f"{r},{c}",
                                 fill=_C_TEXT_COORD, font=("Segoe UI", 8, "bold"))

    def _draw_robot(self):
        if self._oval_id:      self.canvas.delete(self._oval_id)
        if self._robot_lbl_id: self.canvas.delete(self._robot_lbl_id)

        r, c = self.robot_pos
        x1 = self._PX + c * self.CELL + 9
        y1 = self._PY + r * self.CELL + 9
        x2, y2 = x1 + self.CELL - 18, y1 + self.CELL - 18

        self._oval_id = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=_C_ROBOT, outline="white", width=2)
        self._robot_lbl_id = self.canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text="R", fill="white", font=("Segoe UI", 14, "bold"))

    # ══════════════════════════════════════════════════════════════════════
    #  LOGIC
    # ══════════════════════════════════════════════════════════════════════
    def start_cleaning(self):
        self.log_text.delete("1.0", "end")
        self.visited = []

        name = self.algo_var.get()
        self.lbl_algo.config(text=f"Thuật toán: {name}")
        self.log(f"▶  Bắt đầu: {name}")

        algo  = self._ALGO_MAP[name]()
        self.environment = GridEnvironment([r[:] for r in self.original_grid])
        agent = VacuumAgent(self.environment, algo, self.robot_pos)
        self.path = agent.run()

        self.environment = GridEnvironment([r[:] for r in self.original_grid])
        self._animate(0)

    def _animate(self, idx):
        if idx >= len(self.path):
            self.lbl_status.config(text="✔  Hoàn thành", fg=_GREEN)
            self.log("✔  Robot hoàn thành nhiệm vụ!")
            return

        pos = self.path[idx]
        self.robot_pos = pos
        if pos not in self.visited:
            self.visited.append(pos)
        self.environment.clean(pos)
        self.draw_grid()

        self.lbl_status.config(text=f"●  Robot tại {pos}", fg=_AMBER)
        self.lbl_steps.config(text=f"Bước: {idx + 1}")
        self.log(f"  → {pos}")

        self.root.after(self.ANIM, lambda: self._animate(idx + 1))

    def reset_environment(self):
        self._reset_state()
        self.draw_grid()
        self.lbl_status.config(text="●  Đã reset", fg=_GREEN)
        self.lbl_steps.config(text="Bước: 0")
        self.lbl_algo.config(text="")
        self.log_text.delete("1.0", "end")
        self.log("↺  Reset môi trường")

    def log(self, msg):
        self.log_text.insert("end", f"{msg}\n")
        self.log_text.see("end")