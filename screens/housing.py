import tkinter as tk
from tkinter import Frame, Label
import os
from data_handler import get_affordable_houses

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseScreen(Frame):

    def __init__(self, master, on_close=None):
        super().__init__(master)
        self.on_close = on_close
        self.configure(bg="white")


class HousingScreen(BaseScreen):

    HOUSE_IMAGES = [
        os.path.join(BASE_DIR, "Images", "image1.png"),
        os.path.join(BASE_DIR, "Images", "image2.png"),
        os.path.join(BASE_DIR, "Images", "image3.png"),
        os.path.join(BASE_DIR, "Images", "image4.png"),
        os.path.join(BASE_DIR, "Images", "image5.png"),
    ]

    WATER_ICON = os.path.join(BASE_DIR, "Images", "water.png")
    LIGHT_ICON = os.path.join(BASE_DIR, "Images", "light.png")

    def __init__(self, master, state_name,
                 open_details,
                 open_saved,
                 open_bookings,
                 open_feedback):

        super().__init__(master)

        self.state_name = state_name
        self.open_details = open_details
        self.open_saved = open_saved
        self.open_bookings = open_bookings
        self.open_feedback = open_feedback

        self.house_data = []
        self.images = []

        self.water_icon = None
        self.light_icon = None

        self._load_houses()
        self._load_images()
        self.build_content()

    # ================= LOAD DATA =================
    def _load_houses(self):

        df = get_affordable_houses(self.state_name)

        if df is None or df.empty:
            self.house_data = []
            return

        if "town" in df.columns:
            df["city"] = df["town"]

        df["house_type"] = df["title"]

        df = df.head(5)

        self.house_data = df.to_dict("records")

    # ================= LOAD IMAGES =================
    def _load_images(self):

        for path in self.HOUSE_IMAGES:
            try:
                img = tk.PhotoImage(file=path).subsample(3, 3)
                self.images.append(img)
            except:
                self.images.append(None)

        try:
            self.water_icon = tk.PhotoImage(file=self.WATER_ICON).subsample(10, 10)
        except:
            self.water_icon = None

        try:
            self.light_icon = tk.PhotoImage(file=self.LIGHT_ICON).subsample(10, 10)
        except:
            self.light_icon = None

    # ================= UI =================
    def build_content(self):

        Label(
            self,
            text=f"{self.state_name} Houses",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

        container = Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scroll_frame = Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        )

        for i, house in enumerate(self.house_data):
            self._create_card(scroll_frame, house, i)

    # ================= CARD =================
    def _create_card(self, parent, house, index):

        card = Frame(parent, bg="#f7f7f7", bd=1, relief="solid")
        card.pack(fill="x", padx=10, pady=8)

        inner = Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        # IMAGE
        img = self.images[index % len(self.images)]

        img_label = Label(inner, bg="white")
        img_label.pack(side="left", padx=8)

        if img:
            img_label.config(image=img)
            img_label.image = img
        else:
            img_label.config(text="No Image")

        # INFO
        info = Frame(inner, bg="white")
        info.pack(side="left", fill="both", expand=True)

        Label(
            info,
            text=house["house_type"],
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        Label(
            info,
            text=f"₦{int(house['yearly_price']):,}/year",
            fg="green",
            bg="white"
        ).pack(anchor="w")

        Label(
            info,
            text=house.get("city", ""),
            fg="gray",
            bg="white"
        ).pack(anchor="w")

        # ICONS
        icon_row = Frame(info, bg="white")
        icon_row.pack(anchor="w", pady=5)

        if self.water_icon:
            Label(icon_row, image=self.water_icon, text=" Water",
                  compound="left", bg="white").pack(side="left", padx=5)

        if self.light_icon:
            Label(icon_row, image=self.light_icon, text=" Light",
                  compound="left", bg="white").pack(side="left")

        # CLICK → DETAILS
        card.bind("<Button-1>", lambda e, h=house: self.open_details(h))
        inner.bind("<Button-1>", lambda e, h=house: self.open_details(h))
        img_label.bind("<Button-1>", lambda e, h=house: self.open_details(h))
        info.bind("<Button-1>", lambda e, h=house: self.open_details(h))

