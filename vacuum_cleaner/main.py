import tkinter as tk
from ui.vacuum_ui import VacuumUI

def main():
    root = tk.Tk()
    app = VacuumUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()