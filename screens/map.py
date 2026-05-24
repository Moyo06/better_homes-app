import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class MapScreen:

    def __init__(self, root, show_houses, show_saved, show_bookings, show_feedback):

        self.root = root

        # CALLBACK FUNCTIONS
        self.open_houses = show_houses
        self.open_saved = show_saved
        self.open_bookings = show_bookings
        self.open_feedback = show_feedback

        # =========================
        # IMAGE PATH
        # =========================

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        self.map_path = os.path.join(
            BASE_DIR,
            "Images",
            "nigeria_map.png"
        )

        # =========================
        # MAIN FRAME
        # =========================

        self.main_frame = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # =========================
        # CANVAS
        # =========================

        self.canvas = tk.Canvas(
            self.main_frame,
            width=430,
            height=850,
            bg="#f5f5f5",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # =========================
        # MAP IMAGE
        # =========================

        try:

            img = Image.open(self.map_path)

            img = img.resize((430, 700))

            self.map_image = ImageTk.PhotoImage(img)

            self.canvas.create_image(
                0,
                0,
                image=self.map_image,
                anchor="nw"
            )

        except Exception as e:

            print("Map image error:", e)

            self.canvas.create_text(
                215,
                350,
                text="Nigeria Map",
                font=("Arial", 25, "bold")
            )

        # =========================
        # TITLE
        # =========================

        tk.Label(
            self.main_frame,
            text="Find Better Homes",
            font=("Arial", 16, "bold"),
            bg="white"
        ).place(
            relx=0.5,
            y=10,
            anchor="n"
        )

        # =========================
        # STATES
        # =========================

        self.states = [
            "Select A Location",
            "Lagos",
            "Abuja",
            "Oyo",
            "Ogun",
            "Anambra",
            "Edo"
        ]

        self.selected_state = tk.StringVar()

        self.search_box = ttk.Combobox(
            self.main_frame,
            textvariable=self.selected_state,
            values=self.states,
            state="readonly",
            font=("Arial", 12)
        )

        self.search_box.place(
            relx=0.5,
            y=50,
            anchor="n",
            width=250
        )

        self.search_box.bind(
            "<<ComboboxSelected>>",
            self.search_selected
        )

        # =========================
        # VIEW LOCATION BUTTON
        # =========================

        self.location_btn = tk.Button(
            self.main_frame,
            text="View Locations",
            bg="white",
            fg="green",
            font=("Arial", 11, "bold"),
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.go_to_selected_state
        )

        # hidden initially
        self.location_btn.place_forget()

        # =========================
        # CREATE UI
        # =========================

        self.create_green_dots()
        self.create_red_dots()
        self.create_legend()
        self.create_bottom_menu()

    # =========================
    # SHOW VIEW LOCATION BUTTON
    # =========================

    def show_view_locations(self, x, y, state):

        self.selected_state.set(state)

        self.location_btn.place(
            x=x,
            y=y
        )

    # =========================
    # OPEN STATE HOUSES
    # =========================

    def go_to_selected_state(self):

        state = self.selected_state.get()

        if state != "Select A Location":

            self.open_houses(state)

    # =========================
    # GREEN DOTS
    # =========================

    def create_green_dots(self):

        # LAGOS
        lagos = self.canvas.create_oval(
            110, 477, 120, 487,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            lagos,
            "<Button-1>",
            lambda e: self.show_view_locations(140, 470, "Lagos")
        )

        # OYO
        oyo = self.canvas.create_oval(
            130, 355, 150, 375,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            oyo,
            "<Button-1>",
            lambda e: self.show_view_locations(160, 350, "Oyo")
        )

        # ABUJA
        abuja = self.canvas.create_oval(
            335, 330, 355, 350,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            abuja,
            "<Button-1>",
            lambda e: self.show_view_locations(250, 360, "Abuja")
        )

        # OGUN
        ogun = self.canvas.create_oval(
            105, 430, 125, 450,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            ogun,
            "<Button-1>",
            lambda e: self.show_view_locations(130, 425, "Ogun")
        )

        # EDO
        edo = self.canvas.create_oval(
            245, 470, 265, 490,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            edo,
            "<Button-1>",
            lambda e: self.show_view_locations(270, 465, "Edo")
        )

        # ANAMBRA
        anambra = self.canvas.create_oval(
            323, 482, 333, 492,
            fill="green",
            outline="black"
        )

        self.canvas.tag_bind(
            anambra,
            "<Button-1>",
            lambda e: self.show_view_locations(250, 510, "Anambra")
        )

    # =========================
    # RED DOTS
    # =========================

    def create_red_dots(self):

        self.canvas.create_oval(
            170, 120, 190, 140,
            fill="red",
            outline="black"
        )

        self.canvas.create_oval(
            350, 250, 370, 270,
            fill="red",
            outline="black"
        )

        self.canvas.create_oval(
            340, 545, 360, 565,
            fill="red",
            outline="black"
        )

    # =========================
    # LEGEND
    # =========================

    def create_legend(self):

        self.canvas.create_oval(
            20, 650, 35, 665,
            fill="green",
            outline="black"
        )

        self.canvas.create_text(
            110,
            657,
            text="Less Crowded Area",
            font=("Arial", 10)
        )

        self.canvas.create_oval(
            20, 680, 35, 695,
            fill="red",
            outline="black"
        )

        self.canvas.create_text(
            105,
            687,
            text="Overcrowded Area",
            font=("Arial", 10)
        )

    # =========================
    # SEARCH
    # =========================

    def search_selected(self, event):

        state = self.selected_state.get()

        positions = {
            "Lagos": (140, 470),
            "Oyo": (160, 350),
            "Abuja": (250, 360),
            "Ogun": (130, 425),
            "Edo": (270, 465),
            "Anambra": (250, 510)
        }

        if state in positions:

            x, y = positions[state]

            self.show_view_locations(x, y, state)

    # =========================
    # BOTTOM MENU
    # =========================

    def create_bottom_menu(self):

        bottom_frame = tk.Frame(
            self.main_frame,
            bg="white",
            height=90
        )

        bottom_frame.pack(
            side="bottom",
            fill="x"
        )

        tk.Button(
            bottom_frame,
            text="⌂\nHome",
            font=("Arial", 11),
            bd=0,
            bg="white"
        ).pack(
            side="left",
            expand=True
        )

        tk.Button(
            bottom_frame,
            text="♥\nSaved",
            font=("Arial", 11),
            bd=0,
            bg="white",
            command=self.open_saved
        ).pack(
            side="left",
            expand=True
        )

        tk.Button(
            bottom_frame,
            text="📅\nBookings",
            font=("Arial", 11),
            bd=0,
            bg="white",
            command=self.open_bookings
        ).pack(
            side="left",
            expand=True
        )

        tk.Button(
            bottom_frame,
            text="⭐\nFeedback",
            font=("Arial", 11),
            bd=0,
            bg="white",
            command=self.open_feedback
        ).pack(
            side="left",
            expand=True
        )
