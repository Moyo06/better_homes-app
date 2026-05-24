


from tkinter import *
from PIL import Image, ImageTk



class SplashScreen:

    def __init__(self):

       
        self.root = Tk()

       
        self.root.title("Real Estate App")
        self.root.geometry("400x700")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

   
        self.__image_path = "splash.png"

       
        self.create_widgets()

    def create_widgets(self):

        image = Image.open(self.__image_path)

        
        image = image.resize((360, 640))

     
        self.photo = ImageTk.PhotoImage(image)

      
        image_label = Label(
            self.root,
            image=self.photo,
            bg="white"
        )

        image_label.pack(pady=10)


        start_button = Button(
            self.root,
            text="Get Started",
            font=("Arial", 14, "bold"),
            bg="darkgreen",
            fg="white",
            padx=20,
            pady=10,
            command=self.button_click
        )

        start_button.place(x=120, y=550)

    def button_click(self):
        pass
        

    def run(self):

        self.root.mainloop()



app = SplashScreen()


app.run()