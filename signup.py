from tkinter import *
from PIL import Image, ImageTk
import hashlib
import login
from message import custom_message_box
from sound import play_sound
import database

def hash_password(password):
    salt = "a_random_salt"
    return hashlib.sha256((salt + password).encode()).hexdigest()

def on_click():
    play_sound("click")

def submit_form(entry_username, entry_password, signup_window, root):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        custom_message_box("All fields are required!", "error")
        return

    hashed_password = hash_password(password)
    result = database.add_user(username, hashed_password)

    if result == "User registered successfully!":
        custom_message_box("signup successful!", "success")
        entry_username.delete(0, END)
        entry_password.delete(0, END)
        signup_window.destroy()
        login.open_login_page(root)
    else:
        custom_message_box(result, "error")

def open_signup_page(root):
    signup_window = Toplevel(root)
    signup_window.geometry('800x480+230+130')
    signup_window.title("Sign Up Page")
    signup_window.overrideredirect(True)


    signup_bg_image = Image.open('images/sihnupbg.png')
    signup_bg_image = signup_bg_image.resize((850, 500), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(signup_bg_image)
    background_label = Label(signup_window, image=AppBg, bd=0, highlightthickness=0)
    background_label.image = AppBg
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    entry_username = Entry(signup_window, font=("Arial", 18))
    entry_username.place(x=480, y=165)
    entry_password = Entry(signup_window, show="*", font=("Arial", 18))
    entry_password.place(x=480, y=270)


    submit_button = Button(
        signup_window,
        text="Sign Up",
        font=("Arial", 12),
        width=35,
        height=2,
        bg="green",
        fg="white",
        command=lambda: [on_click(), submit_form(entry_username, entry_password, signup_window, root)]
    )
    submit_button.place(x=455, y=330)


    text_label = Label(signup_window, text="I already have an account?", font=("Arial", 12))
    text_label.place(x=490, y=400)
    login_link = Label(signup_window, text="Login", fg="green", bg="#fed52d", cursor="hand2")
    login_link.config(font=("Arial", 15, "bold"))
    login_link.place(x=680, y=400)
    login_link.bind("<Button-1>", lambda e: [signup_window.destroy(), login.open_login_page(root)])
