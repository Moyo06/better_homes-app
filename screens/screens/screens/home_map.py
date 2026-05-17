import tkinter as tk

class HomeScreen(tk.Frame):
  def __init__(self, app):
      super().__init__(app.root)
      tk.Label(self, text="Home Map Screen").pack()
    
