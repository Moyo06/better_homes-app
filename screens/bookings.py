
import tkinter as tk
from PIL import Image, ImageTk


class BookingsListScreen:

    def __init__(self, root, booked_houses, open_details):

        self.root = root
        self.booked_houses = booked_houses
        self.open_details = open_details

        self.root.configure(bg="#f4f5f7")

        self.build_ui()



    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Booked Tours",
            font=("Arial", 20, "bold"),
            bg="#f4f5f7"
        )

        title.pack(pady=20)

        if len(self.booked_houses) == 0:

            tk.Label(
                self.root,
                text="No bookings yet 📅",
                font=("Arial", 14),
                bg="#f4f5f7",
                fg="gray"
            ).pack(pady=50)

            return


        for booking in self.booked_houses:

            self.create_booking_card(booking)


    def create_booking_card(self, booking):

        card = tk.Frame(
            self.root,
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

            img = Image.open(booking["image1"])

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
            text=booking["title"],
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            details,
            text=booking["state"],
            font=("Arial", 11),
            bg="white",
            fg="gray"
        ).pack(anchor="w", pady=3)

        tk.Label(
            details,
            text=f"{booking['date']} at {booking['time']}",
            font=("Arial", 11),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            details,
            text=booking["phone"],
            font=("Arial", 11),
            bg="white",
            fg="gray"
        ).pack(anchor="w", pady=(0, 5))

        view_btn = tk.Button(
            card,
            text="View",
            bg="darkgreen",
            fg="white",
            command=lambda: self.open_details(booking)
        )

        view_btn.pack(
            side="right",
            padx=10
        )
