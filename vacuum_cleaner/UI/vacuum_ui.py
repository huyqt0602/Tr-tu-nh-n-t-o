import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from environment.grid_environment import GridEnvironment

from algorithms.bfs_algorithm import BFSAlgorithm
from algorithms.dfs_algorithm import DFSAlgorithm
from algorithms.ids_algorithm import IDSAlgorithm
from algorithms.ucs_algorithm import UCSAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.astar_algorithm import AStarAlgorithm

from agents.vacuum_agent import VacuumAgent

class VacuumUI:

    CELL_SIZE = 90

    def __init__(self, root):

        self.root = root

        self.root.title("ROBOT HÚT BỤI AI")

        self.root.geometry("1450x850")

        self.root.configure(bg="#dfe6e9")

        # Môi trường ban đầu
        self.original_grid = [
            [0, 1, 0, 0],
            [1, -1, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 1]
        ] 

        self.environment = GridEnvironment(
            [row[:] for row in self.original_grid]
        )

        self.robot_position = (0, 0) # Vị trí bắt đầu của robot

        self.visited_cells = []

        self.path = []

        self.create_layout()

        self.robot_draw = None
        self.robot_text = None


        self.draw_grid()

    # UI
    def create_layout(self):

        self.main_frame = tk.Frame(
            self.root,
            bg="#dfe6e9"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # LEFT PANEL
        self.sidebar = tk.Frame(
            self.main_frame,
            bg="#2d3436",
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        title = tk.Label(
            self.sidebar,
            text="THUẬT TOÁN",
            bg="#2d3436",
            fg="white",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=25)

        self.algorithm_var = tk.StringVar(
            value="BFS"
        )

        for algo in [
            "BFS",
            "DFS",
            "IDS",
            "UCS",
            "GREEDY",
            "A*"
        ]:
            
            button = tk.Radiobutton(
                self.sidebar,
                text=algo,
                variable=self.algorithm_var,
                value=algo,
                indicatoron=False,
                width=12,
                height=2,
                font=("Arial", 15, "bold"),
                bg="#636e72",
                fg="white",
                selectcolor="#00b894",
                activebackground="#00b894",
                activeforeground="white"
            )

            button.pack(pady=10)

        # START BUTTON
        start_button = tk.Button(
            self.sidebar,
            text="BẮT ĐẦU",
            command=self.start_cleaning,
            bg="#00b894",
            fg="white",
            font=("Arial", 15, "bold"),
            width=14,
            height=2,
            relief="flat"
        )

        start_button.pack(pady=(50, 15))

        # RESET BUTTON
        reset_button = tk.Button(
            self.sidebar,
            text="RESET",
            command=self.reset_environment,
            bg="#e17055",
            fg="white",
            font=("Arial", 15, "bold"),
            width=14,
            height=2,
            relief="flat"
        )

        reset_button.pack()

        # CENTER
        self.center_frame = tk.Frame(
            self.main_frame,
            bg="#dfe6e9"
        )

        self.center_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        title = tk.Label(
            self.center_frame,
            text="MÔ PHỎNG ROBOT HÚT BỤI",
            bg="#dfe6e9",
            fg="#2d3436",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=20)

        self.canvas = tk.Canvas(
            self.center_frame,
            width=750,
            height=650,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack()

        # RIGHT PANEL
        self.right_panel = tk.Frame(
            self.main_frame,
            bg="#b2bec3",
            width=320
        )

        self.right_panel.pack(
            side="right",
            fill="y"
        )

        self.right_panel.pack_propagate(False)

        log_title = tk.Label(
            self.right_panel,
            text="NHẬT KÝ HOẠT ĐỘNG",
            bg="#b2bec3",
            fg="#2d3436",
            font=("Arial", 20, "bold")
        )

        log_title.pack(pady=20)

        self.log_text = ScrolledText(
            self.right_panel,
            font=("Consolas", 11)
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # BOTTOM BAR
        self.bottom_bar = tk.Frame(
            self.root,
            bg="#2d3436",
            height=55
        )

        self.bottom_bar.pack(
            fill="x",
            side="bottom"
        )

        self.info_label = tk.Label(
            self.bottom_bar,
            text="Sẵn sàng",
            bg="#2d3436",
            fg="white",
            font=("Arial", 14, "bold")
        )

        self.info_label.pack(
            side="left",
            padx=20
        )

        self.step_label = tk.Label(
            self.bottom_bar,
            text="Số bước: 0",
            bg="#2d3436",
            fg="#55efc4",
            font=("Arial", 13)
        )

        self.step_label.pack(
            side="left",
            padx=30
        )

    # DRAW GRID
    def draw_grid(self):

        self.canvas.delete("all")

        for r in range(self.environment.rows):
            for c in range(self.environment.cols):

                x1 = c * self.CELL_SIZE + 80
                y1 = r * self.CELL_SIZE + 40

                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                value = self.environment.grid[r][c]

                color = "#ecf0f1"

                # Ô đã đi
                if (r, c) in self.visited_cells:
                    color = "#74b9ff"

                # Bụi
                if value == 1:
                    color = "#f1c40f"

                # Tường
                if value == -1:
                    color = "#2d3436"

                # Vẽ ô
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#636e72",
                    width=2
                )

                # Text bụi
                if value == 1:

                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text="BỤI",
                        font=("Arial", 11, "bold"),
                        tags=f"dirt_{r}_{c}"
                    )

                # Text tường
                elif value == -1:

                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text="X",
                        fill="white",
                        font=("Arial", 22, "bold")
                    )

        # Vẽ robot
        self.draw_robot()

    # DRAW ROBOT
    def draw_robot(self):

        # Xóa robot cũ
        if self.robot_draw:
            self.canvas.delete(self.robot_draw)

        if self.robot_text:
            self.canvas.delete(self.robot_text)

        r, c = self.robot_position

        x1 = c * self.CELL_SIZE + 80
        y1 = r * self.CELL_SIZE + 40

        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE

        # Vẽ robot
        self.robot_draw = self.canvas.create_oval(
            x1 + 10,
            y1 + 10,
            x2 - 10,
            y2 - 10,
            fill="#0984e3",
            outline="white",
            width=3
        )

        self.robot_text = self.canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="R",
            fill="white",
            font=("Arial", 20, "bold")
        )

    # GET ALGORITHM
    def get_algorithm(self):

        algorithms = {
            "BFS": BFSAlgorithm,
            "DFS": DFSAlgorithm,
            "IDS": IDSAlgorithm,
            "UCS": UCSAlgorithm,
            "GREEDY": GreedyAlgorithm,
            "A*": AStarAlgorithm
        }

        selected = self.algorithm_var.get()

        return algorithms[selected]()

    # START
    def start_cleaning(self):

        self.log_text.delete("1.0", "end")

        self.visited_cells = []

        algorithm = self.get_algorithm()

        self.log(
            f"Khởi động thuật toán {self.algorithm_var.get()}"
        )

        agent = VacuumAgent(
            self.environment,
            algorithm,
            self.robot_position
        )

        self.path = agent.run()

        self.environment = GridEnvironment(
            [row[:] for row in self.original_grid]
        )

        self.animate(0)
        
    # ANIMATION
    def animate(self, index):

        if index >= len(self.path):

            self.info_label.config(
                text="Hoàn thành làm sạch"
            )

            self.log(
                "Robot hoàn thành nhiệm vụ"
            )

            return

        # Vị trí mới
        position = self.path[index]

        self.robot_position = position

        # Lưu ô đã đi
        if position not in self.visited_cells:
            self.visited_cells.append(position)

        r, c = position

        # Làm sạch ô
        self.environment.clean(position)

        # Vẽ lại toàn bộ grid
        self.draw_grid()

        # Status
        self.info_label.config(
            text=f"Robot đang ở: {position}"
        )

        self.step_label.config(
            text=f"Số bước: {index + 1}"
        )

        self.log(
            f"Di chuyển tới {position}"
        )

        self.root.after(
            250,
            lambda: self.animate(index + 1)
        )

    # RESET
    def reset_environment(self):

        self.environment = GridEnvironment(
            [row[:] for row in self.original_grid]
        )

        self.robot_position = (0, 0)

        self.visited_cells = []

        self.path = []

        self.robot_draw = None
        self.robot_text = None

        self.draw_grid()

        self.info_label.config(
            text="Đã reset môi trường"
        )

        self.step_label.config(
            text="Số bước: 0"
        )

        self.log_text.delete("1.0", "end")

        self.log("Reset môi trường")

    # LOG
    def log(self, message):

        self.log_text.insert(
            "end",
            f"> {message}\n"
        )

        self.log_text.see("end")