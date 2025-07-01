import tkinter as tk
from gui.dashboard_gui import CarDashboard

def main():
    root = tk.Tk()
    dashboard = CarDashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        dashboard.on_closing()

if __name__ == "__main__":
    main()
