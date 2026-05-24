import tkinter as tk
from PIL import Image, ImageTk

class ConfirmationScreen:
    def __init__(self, booking_data, previous_root=None):
        self.booking_data = booking_data
        self.previous_root = previous_root
        
        self.root = tk.Tk()
        self.root.title("Booking Confirmed")
        self.root.geometry("550x750")
        self.root.configure(bg="#f4f5f7")
        self.root.resizable(False, False)
        
        self.show_confirmation()
        self.root.mainloop()

    def show_confirmation(self):
        frame = tk.Frame(self.root, bg="#f4f5f7")
        frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        tk.Label(frame, text="✓", font=("Segoe UI", 60, "bold"), fg="#16a34a", bg="#f4f5f7").pack()
        tk.Label(frame, text="Tour Booked!", font=("Segoe UI", 26, "bold"), fg="#16a34a", bg="#f4f5f7").pack(pady=(0, 10))
        tk.Label(frame, text="Your house tour has been successfully booked.", font=("Segoe UI", 12), fg="#4b5563", bg="#f4f5f7").pack(pady=(0, 25))
        
        try:
            img = Image.open(self.booking_data["image_path"])
            img = img.resize((420, 220), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(frame, image=photo, bg="#f4f5f7")
            image_label.image = photo
            image_label.pack(pady=(0, 20))
        except:
            pass
        
        card = tk.Frame(frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=(0, 25))
        
        tk.Label(card, text=f"{self.booking_data['date']} • {self.booking_data['time']}", font=("Segoe UI", 14, "bold"), bg="white", fg="#111827").pack(anchor="w", padx=20, pady=(20, 10))
        tk.Label(card, text=self.booking_data["property_name"], font=("Segoe UI", 16, "bold"), bg="white", fg="#111827").pack(anchor="w", padx=20, pady=(0, 5))
        tk.Label(card, text=self.booking_data["property_location"], font=("Segoe UI", 11), bg="white", fg="#6b7280", wraplength=400, justify="left").pack(anchor="w", padx=20, pady=(0, 20))
        
        tk.Label(frame, text=f"Confirmation sent to: {self.booking_data['phone']}", font=("Segoe UI", 10), fg="#9ca3af", bg="#f4f5f7").pack(pady=(0, 25))
        
        home_btn = tk.Button(frame, text="Back to Home", font=("Segoe UI", 13, "bold"), bg="#16a34a", fg="white", activebackground="#15803d", activeforeground="white", relief="raised", bd=2, cursor="hand2", pady=12, command=self.go_home)
        home_btn.pack(fill="x")

    def go_home(self):
        self.root.destroy()
        if self.previous_root:
            self.previous_root.destroy()
        from booking import BookingApp
        BookingApp()

if __name__ == "__main__":
    sample_data = {
        "property_name": "3 Bedroom Terrace",
        "property_location": "97 Adeniyi Crescent, Mabushi, Abuja",
        "property_price": "₦850,000/year",
        "date": "May 20, 2026",
        "time": "10:00 AM",
        "phone": "+1234567890",
        "image_path": "images/apartment1.jpg"
    }
    ConfirmationScreen(sample_data)
