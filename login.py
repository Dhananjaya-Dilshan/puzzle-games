from tkinter import *
from PIL import Image, ImageTk
import signup
import dashboard
from sound import play_sound
from message import custom_message_box
import database

def on_click():
    play_sound("click")

def verify_login(entry_username, entry_password, login_window):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        custom_message_box("All fields are required!", "error")
        return

    hashed_password = signup.hash_password(password)
    result = database.verify_user(username, hashed_password)
    if result is True:
        custom_message_box("Login successful!", "success")
        dashboard.open_dashboard(username, password)
    elif result == "Error":
        custom_message_box(result, "error")
    else:
        custom_message_box("Invalid username or password.", "error")

def open_login_page(root):
    login_window = Toplevel(root)
    login_window.geometry('800x480+230+130')
    login_window.title("Login Page")
    login_window.overrideredirect(True)

    login_bg_image = Image.open('images/loginbg.png')
    login_bg_image = login_bg_image.resize((850, 500), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(login_bg_image)
    background_label = Label(login_window, image=AppBg, bd=0, highlightthickness=0)
    background_label.image = AppBg  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    entry_username = Entry(login_window, font=("Arial", 18))
    entry_username.place(x=480, y=170)
    entry_password = Entry(login_window, show="*", font=("Arial", 18))
    entry_password.place(x=480, y=290)


    login_button = Button(
        login_window,
        text="Login",
        font=("Arial", 12),
        width=35,
        height=2,
        bg="green",
        fg="white",
        command=lambda: [on_click(), verify_login(entry_username, entry_password, login_window)]
    )
    login_button.place(x=455, y=340)


    text_label = Label(login_window, text="I don't have an account?", font=("Arial", 12))
    text_label.place(x=495, y=400)
    signup_link = Label(login_window, text="Signup", fg="green", bg="#fed52d", cursor="hand2")
    signup_link.config(font=("Arial", 15, "bold"))
    signup_link.place(x=675, y=400)
    signup_link.bind("<Button-1>", lambda e: [login_window.destroy(), signup.open_signup_page(root)])
