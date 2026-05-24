import tkinter as tk

COLOR_PRIMARY_GREEN = "#2D6A4F"
COLOR_BG_WHITE      = "#FFFFFF"
COLOR_BG_LIGHT_GRAY = "#F5F5F5"
COLOR_TEXT_DARK     = "#111111"
COLOR_TEXT_MUTED    = "#666666"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Better Places, Better Lives")
        self.geometry("380x680")
        self.configure(bg=COLOR_BG_WHITE)
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.current_screen = None
        self.screens = {}