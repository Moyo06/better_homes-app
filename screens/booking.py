import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime

class BookingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Property Tour Booking")
        self.root.geometry("550x750")
        self.root.configure(bg="#f4f5f7")
        self.root.resizable(False, False)
        
        self.main_canvas = tk.Canvas(self.root, bg="#f4f5f7", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#f4f5f7")
        self.scrollable_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.bind_all("<MouseWheel>", lambda event: self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        
        self.booking_data = {}
        self.current_frame = None
        self.current_image_label = None
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "images")
        
        self.locations = {
            "97 Adeniyi Crescent, Mabushi, Abuja": {"image": os.path.join(images_dir, "apartment1.jpg"), "bedrooms": "3 Bedroom Terrace", "price": "₦850,000/year"},
            "98 Peace Road, Lekki, Anambara": {"image": os.path.join(images_dir, "apartment2.jpg"), "bedrooms": "2 Bedroom Flat", "price": "₦1,200,000/year"},
            "67 Unity Close, Oredo, Edo": {"image": os.path.join(images_dir, "apartment3.jpg"), "bedrooms": "4 Bedroom Duplex", "price": "₦2,500,000/year"},
            "37 Adeniyi Crescent, Lekki, Lagos": {"image": os.path.join(images_dir, "apartment4.jpg"), "bedrooms": "2 Bedroom Apartment", "price": "₦1,500,000/year"},
            "44 Peace Road, Mowe Ofada, Ogun": {"image": os.path.join(images_dir, "apartment5.jpg"), "bedrooms": "3 Bedroom Bungalow", "price": "₦950,000/year"},
            "47 Adeola Street, Ibadan, Oyo": {"image": os.path.join(images_dir, "apartment6.jpg"), "bedrooms": "2 Bedroom Apartment", "price": "₦750,000/year"}
        }
        
        self.selected_location = tk.StringVar(value=list(self.locations.keys())[0])
        self.selected_date = tk.StringVar(value="May 20, 2026")
        self.selected_time = tk.StringVar(value="10:00 AM")
        
        self.show_booking_screen()
        self.root.mainloop()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_booking_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.scrollable_frame, bg="#f4f5f7")
        self.current_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        tk.Label(self.current_frame, text="Book a House Tour", font=("Segoe UI", 24, "bold"), bg="#f4f5f7", fg="#111827").pack(pady=(0, 20))
        
        property_card = tk.Frame(self.current_frame, bg="#edf7ee", bd=1, relief="solid")
        property_card.pack(fill="x", pady=(0, 25))
        
        top_frame = tk.Frame(property_card, bg="#edf7ee")
        top_frame.pack(fill="x", padx=15, pady=15)
        
        self.current_image_label = tk.Label(top_frame, bg="#edf7ee")
        self.current_image_label.pack(side="left", padx=(0, 15))
        
        details_frame = tk.Frame(top_frame, bg="#edf7ee")
        details_frame.pack(side="left", fill="both", expand=True)
        
        self.property_name_label = tk.Label(details_frame, font=("Segoe UI", 20, "bold"), bg="#edf7ee", fg="#111827")
        self.property_name_label.pack(anchor="w", pady=(15, 5))
        
        self.property_location_label = tk.Label(details_frame, font=("Segoe UI", 12), bg="#edf7ee", fg="#6b7280")
        self.property_location_label.pack(anchor="w", pady=(0, 10))
        
        self.property_price_label = tk.Label(details_frame, font=("Segoe UI", 16, "bold"), bg="#edf7ee", fg="#16a34a")
        self.property_price_label.pack(anchor="w")
        
        self.update_apartment_image()
        self.update_property_details()
        
        tk.Label(self.current_frame, text="Select Location", font=("Segoe UI", 12, "bold"), bg="#f4f5f7", fg="#1f2937").pack(anchor="w", pady=(0, 8))
        location_dropdown = ttk.Combobox(self.current_frame, textvariable=self.selected_location, values=list(self.locations.keys()), state="readonly", font=("Segoe UI", 12))
        location_dropdown.pack(fill="x", ipady=8, pady=(0, 25))
        location_dropdown.bind("<<ComboboxSelected>>", self.on_location_change)
        
        tk.Label(self.current_frame, text="Select Date", font=("Segoe UI", 12, "bold"), bg="#f4f5f7", fg="#1f2937").pack(anchor="w", pady=(0, 8))
        date_frame = tk.Frame(self.current_frame, bg="#f4f5f7")
        date_frame.pack(fill="x", pady=(0, 25))
        
        date_entry = tk.Entry(date_frame, textvariable=self.selected_date, font=("Segoe UI", 12), bg="white", fg="#111827", relief="flat", borderwidth=0, highlightcolor="white", highlightbackground="white", highlightthickness=2, state="readonly", readonlybackground="white")
        date_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 10))
        
        calendar_btn = tk.Button(date_frame, text="📅", font=("Segoe UI", 14), bg="white", fg="#111827", relief="solid", borderwidth=1, cursor="hand2", command=self.show_calendar)
        calendar_btn.pack(ipadx=15, ipady=6)
        
        tk.Label(self.current_frame, text="Select Time", font=("Segoe UI", 12, "bold"), bg="#f4f5f7", fg="#1f2937").pack(anchor="w", pady=(0, 8))
        time_dropdown = ttk.Combobox(self.current_frame, textvariable=self.selected_time, values=["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"], state="readonly", font=("Segoe UI", 12))
        time_dropdown.pack(fill="x", ipady=8, pady=(0, 25))
        
        tk.Label(self.current_frame, text="Your Phone Number", font=("Segoe UI", 12, "bold"), bg="#f4f5f7", fg="#1f2937").pack(anchor="w", pady=(0, 8))
        self.phone_entry = tk.Entry(self.current_frame, font=("Segoe UI", 13), bg="white", fg="#111827", insertbackground="#111827", relief="flat", borderwidth=0, highlightcolor="white", highlightbackground="white", highlightthickness=2)
        self.phone_entry.pack(fill="x", ipady=14, pady=(0, 30))
        
        confirm_btn = tk.Button(self.current_frame, text="Confirm Booking", font=("Segoe UI", 15, "bold"), bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white", relief="raised", bd=2, cursor="hand2", pady=14, command=self.process_booking)
        confirm_btn.pack(fill="x")
        
        tk.Label(self.current_frame, text="🔒 Your information is safe with us.", font=("Segoe UI", 10), bg="#f4f5f7", fg="#9ca3af").pack(pady=(20, 0))

    def on_location_change(self, event):
        self.update_apartment_image()
        self.update_property_details()

    def update_apartment_image(self):
        location = self.selected_location.get()
        image_path = self.locations[location]["image"]
        try:
            img = Image.open(image_path)
            img = img.resize((170, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.current_image_label.config(image=photo)
            self.current_image_label.image = photo
        except:
            self.current_image_label.config(text="No Image", font=("Segoe UI", 14), fg="#6b7280")

    def update_property_details(self):
        location = self.selected_location.get()
        details = self.locations[location]
        self.property_name_label.config(text=details["bedrooms"])
        self.property_location_label.config(text=location)
        self.property_price_label.config(text=details["price"])

    def show_calendar(self):
        popup = tk.Toplevel(self.root)
        popup.title("Select Date")
        popup.geometry("300x250")
        popup.configure(bg="#f4f5f7")
        tk.Label(popup, text="Select Tour Date", font=("Segoe UI", 16, "bold"), bg="#f4f5f7", fg="#111827").pack(pady=20)
        frame = tk.Frame(popup, bg="#f4f5f7")
        frame.pack()
        year_spin = tk.Spinbox(frame, from_=2026, to=2028, width=6)
        month_spin = tk.Spinbox(frame, from_=1, to=12, width=4)
        day_spin = tk.Spinbox(frame, from_=1, to=31, width=4)
        year_spin.grid(row=0, column=0, padx=5)
        month_spin.grid(row=0, column=1, padx=5)
        day_spin.grid(row=0, column=2, padx=5)

        def select_date():
            try:
                year = int(year_spin.get())
                month = int(month_spin.get())
                day = int(day_spin.get())
                selected = datetime.date(year, month, day)
                self.selected_date.set(selected.strftime("%B %d, %Y"))
                popup.destroy()
            except:
                messagebox.showerror("Error", "Invalid date")
        
        tk.Button(popup, text="Select", bg="#16a34a", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=8, cursor="hand2", command=select_date).pack(pady=30)

    def process_booking(self):
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Missing Information", "Please enter your phone number!")
            return
        location = self.selected_location.get()
        details = self.locations[location]
        self.booking_data = {
            "property_name": details["bedrooms"],
            "property_location": location,
            "property_price": details["price"],
            "date": self.selected_date.get(),
            "time": self.selected_time.get(),
            "phone": phone,
            "image_path": details["image"]
        }
        from confirmation import ConfirmationScreen
        self.root.withdraw()
        ConfirmationScreen(self.booking_data, self.root)

if __name__ == "__main__":
    BookingApp()
