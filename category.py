from tkinter import *
from PIL import Image, ImageTk
from Game import open_Game
from sound import play_sound

def on_click():
     play_sound("click")

def open_category(root, username):
    category = Toplevel(root)
    category.geometry('800x500+250+70')
    category.title("Category Page")
    category.overrideredirect(True)

    bg_image = Image.open('images/catagory.png').resize((800, 500), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(category, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    category.bg_image = AppBg

    # Fruit
    fruit_image = Image.open('images/fruit.png').resize((350, 50), Image.Resampling.LANCZOS)
    fruit_btn = ImageTk.PhotoImage(fruit_image)
    fruit_button = Button(category, image=fruit_btn, bd=0, highlightthickness=0, command=lambda: [ on_click(), open_Game("fruit", username)])
    fruit_button.place(x=220, y=120)
    category.fruit_btn = fruit_btn

    # Animal
    animal_image = Image.open('images/animal.png').resize((350, 50), Image.Resampling.LANCZOS)
    animal_btn = ImageTk.PhotoImage(animal_image)
    animal_button = Button(category, image=animal_btn, bd=0, highlightthickness=0, command=lambda: [ on_click(), open_Game("animal", username)])
    animal_button.place(x=220, y=235)
    category.animal_btn = animal_btn

    # Vehicle
    vehicle_image = Image.open('images/vehicle.png').resize((350, 50), Image.Resampling.LANCZOS)
    vehicle_btn = ImageTk.PhotoImage(vehicle_image)
    vehicle_button = Button(category, image=vehicle_btn, bd=0, highlightthickness=0, command=lambda: [  open_Game("vehicle", username)])
    vehicle_button.place(x=220, y=350)
    category.vehicle_btn = vehicle_btn
