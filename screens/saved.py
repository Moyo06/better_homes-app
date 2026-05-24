import tkinter as tk
from PIL import Image, ImageTk
import os


class SavedScreen:

    def __init__(self, root, saved_houses, open_details):

        self.root = root
        self.saved_houses = saved_houses
        self.open_details = open_details

        self.root.configure(bg="#f0f0f0")

        self.create_ui()

    # ==========================================
    # UI
    # ==========================================

    def create_ui(self):

        # TITLE
        title = tk.Label(
            self.root,
            text="Saved Homes",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )

        title.pack(pady=20)

        # SCROLLABLE AREA
        container = tk.Frame(self.root, bg="#f0f0f0")

        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container,
            bg="#f0f0f0",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = tk.Frame(
            canvas,
            bg="#f0f0f0"
        )

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================================
        # NO SAVED HOUSES
        # ==========================================

        if len(self.saved_houses) == 0:

            tk.Label(
                scroll_frame,
                text="No saved homes yet ❤️",
                font=("Arial", 14),
                bg="#f0f0f0",
                fg="gray"
            ).pack(pady=50)

            return

        # ==========================================
        # HOUSE CARDS
        # ==========================================

        for house in self.saved_houses:

            self.create_house_card(
                scroll_frame,
                house
            )

    # ==========================================
    # HOUSE CARD
    # ==========================================

    def create_house_card(self, parent, house):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="x",
            padx=15,
            pady=10
        )

        # IMAGE
        try:

            image_path = house["image1"]

            img = Image.open(image_path)

            img = img.resize((120, 90))

            photo = ImageTk.PhotoImage(img)

            image_label = tk.Label(
                card,
                image=photo,
                bg="white"
            )

            image_label.image = photo

            image_label.pack(
                side="left",
                padx=10,
                pady=10
            )

        except:

            image_label = tk.Label(
                card,
                text="No Image",
                bg="white"
            )

            image_label.pack(
                side="left",
                padx=10
            )

        # DETAILS
        details = tk.Frame(
            card,
            bg="white"
        )

        details.pack(
            side="left",
            fill="both",
            expand=True,
            pady=10
        )

        tk.Label(
            details,
            text=house["title"],
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            details,
            text=house["state"],
            font=("Arial", 11),
            bg="white",
            fg="gray"
        ).pack(anchor="w", pady=3)

        tk.Label(
            details,
            text=f"₦{int(house['yearly_price']):,}/year",
            font=("Arial", 13, "bold"),
            fg="green",
            bg="white"
        ).pack(anchor="w")

        # VIEW BUTTON
        view_btn = tk.Button(
            card,
            text="View",
            bg="darkgreen",
            fg="white",
            command=lambda: self.open_details(house)
        )

        view_btn.pack(
            side="right",
            padx=10
        )

