import tkinter as tk
from tkinter import font as tkfont
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")


class DetailsScreen(tk.Frame):

    def __init__(self, root, house, open_booking, add_to_saved, open_saved, go_back):

        super().__init__(root, bg="white")

        self.house = house
        self.open_booking = open_booking
        self.add_to_saved = add_to_saved
        self.open_saved = open_saved
        self.go_back = go_back

        self.liked = False

        self.hero_img = None
        self.extra_imgs = []

        self.hero_label = None
        self.thumb_frame = None

        self.setup_fonts()
        self.load_images()
        self.build_ui()

    # ================= FONTS =================
    def setup_fonts(self):
        f = "Arial"
        self.title_font = tkfont.Font(family=f, size=16, weight="bold")
        self.price_font = tkfont.Font(family=f, size=22, weight="bold")
        self.small_font = tkfont.Font(family=f, size=10)

    # ================= IMAGE LOADER (FORCED SAME SIZE) =================
    def load_and_resize(self, path):
        try:
            img = tk.PhotoImage(file=path)
            return img.subsample(4, 4)   # 🔥 SAME SIZE FOR ALL IMAGES
        except:
            return None

    # ================= IMAGES =================
    def load_images(self):

        # HERO IMAGE
        hero_index = (self.house.get("id", 1) % 5) + 1
        hero_path = os.path.join(IMAGE_DIR, f"image{hero_index}.png")
        self.hero_img = self.load_and_resize(hero_path)

        # EXTRA IMAGES (EXACTLY 4)
        extras = [f"extra image{i}.png" for i in range(1, 9)]
        random.shuffle(extras)

        self.extra_imgs = []
        count = 0

        for img_name in extras:
            if count == 4:
                break

            path = os.path.join(IMAGE_DIR, img_name)
            img = self.load_and_resize(path)

            if img:
                self.extra_imgs.append(img)
                count += 1

    # ================= TOP BAR =================
    def top_bar(self, parent):

        bar = tk.Frame(parent, bg="white")
        bar.pack(fill="x", pady=10)

        tk.Button(
            bar,
            text="← Back",
            bg="white",
            bd=0,
            font=("Arial", 12, "bold"),
            command=self.go_back
        ).pack(side="left", padx=10)

        def toggle_like():
            self.liked = not self.liked
            if self.liked:
                heart.config(text="❤️", fg="red")
                self.add_to_saved(self.house)
            else:
                heart.config(text="🤍", fg="black")

        heart = tk.Button(
            bar,
            text="🤍",
            font=("Arial", 14),
            bg="white",
            bd=0,
            fg="black",
            activeforeground="red",
            command=toggle_like
        )
        heart.pack(side="right", padx=10)

    # ================= SWAP IMAGES =================
    def swap_images(self, index):

        clicked = self.extra_imgs[index]

        # swap
        self.extra_imgs[index] = self.hero_img
        self.hero_img = clicked

        # update hero image
        self.hero_label.config(image=self.hero_img)
        self.hero_label.image = self.hero_img

        # rebuild thumbnails
        for w in self.thumb_frame.winfo_children():
            w.destroy()

        self.build_thumbnails()

    # ================= THUMBNAILS =================
    def build_thumbnails(self):

        for i, img in enumerate(self.extra_imgs):

            lbl = tk.Label(
                self.thumb_frame,
                image=img,
                bg="white",
                cursor="hand2"
            )
            lbl.image = img
            lbl.pack(side="left", padx=5)

            lbl.bind("<Button-1>", lambda e, i=i: self.swap_images(i))

    # ================= UI =================
    def build_ui(self):

        container = tk.Canvas(self, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=container.yview)
        container.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        container.pack(side="left", fill="both", expand=True)

        scroll = tk.Frame(container, bg="white")

        container_window = container.create_window((0, 0), window=scroll, anchor="n")

        container.bind("<Configure>", lambda e: container.itemconfig(container_window, width=e.width))
        scroll.bind("<Configure>", lambda e: container.configure(scrollregion=container.bbox("all")))

        # ================= TOP BAR =================
        self.top_bar(scroll)

        # ================= HERO IMAGE =================
        if self.hero_img:
            self.hero_label = tk.Label(scroll, image=self.hero_img, bg="white")
            self.hero_label.image = self.hero_img
            self.hero_label.pack(pady=10, anchor="center")

        # ================= PRICE =================
        tk.Label(
            scroll,
            text=f"₦{int(self.house.get('yearly_price', 0)):,} / year",
            font=self.price_font,
            fg="green",
            bg="white"
        ).pack(pady=5, anchor="center")

        # ================= TITLE =================
        tk.Label(
            scroll,
            text=self.house.get("title", ""),
            font=self.title_font,
            bg="white"
        ).pack(anchor="center")

        # ================= ADDRESS =================
        tk.Label(
            scroll,
            text=self.house.get("address", ""),
            font=self.small_font,
            bg="white",
            fg="gray"
        ).pack(pady=5, anchor="center")

        # ================= STATS =================
        stats = tk.Frame(scroll, bg="white")
        stats.pack(pady=10)

        items = [
            ("🛏", "Beds", self.house.get("beds", 3)),
            ("🚿", "Baths", self.house.get("baths", 2)),
            ("🚽", "Toilets", self.house.get("toilets", 2)),
            ("🚗", "Parking", self.house.get("parking", 1)),
        ]

        for i, (icon, label, value) in enumerate(items):
            box = tk.Frame(stats, bg="#f2f2f2", width=90, height=80)
            box.grid(row=0, column=i, padx=5)
            box.grid_propagate(False)

            tk.Label(box, text=icon, bg="#f2f2f2").pack()
            tk.Label(box, text=str(value), bg="#f2f2f2", font=("Arial", 12, "bold")).pack()
            tk.Label(box, text=label, bg="#f2f2f2").pack()

        # ================= AMENITIES =================
        amenities = tk.Frame(scroll, bg="white")
        amenities.pack(pady=10)

        items = [
            ("💧", "Water", "Good"),
            ("⚡", "Electricity", "Stable"),
            ("🛣", "Road Score", "6/10"),
        ]

        for i, (icon, name, value) in enumerate(items):
            box = tk.Frame(amenities, bg="white")
            box.grid(row=0, column=i, padx=25)

            tk.Label(box, text=icon, bg="white", font=("Arial", 12)).pack()
            tk.Label(box, text=name, bg="white", font=("Arial", 10)).pack()
            tk.Label(box, text=value, bg="white", font=("Arial", 10, "bold")).pack()

        # ================= THUMBNAILS =================
        tk.Label(
            scroll,
            text="More Images",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(pady=10, anchor="center")

        self.thumb_frame = tk.Frame(scroll, bg="white")
        self.thumb_frame.pack()

        self.build_thumbnails()

        # ================= BOOK BUTTON =================
        tk.Button(
            scroll,
            text="Book House Tour",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: self.open_booking(self.house)
        ).pack(pady=20, anchor="center")