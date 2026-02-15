from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
import os
import pygame
from sound import is_sfx_muted_state

pygame.mixer.init()
is_sfx_muted = False
user_choice = None


def custom_message_box(message, message_type="success", width=600):
    global user_choice
    # Reset choice
    user_choice = None


    msg_box = Toplevel()
    msg_box.overrideredirect(True)
    msg_box.geometry('450x320+450+230')
    msg_box.resizable(False, False)

    if message_type == "success":
        bg_image_path = os.path.join(os.getcwd(), "images", "success.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "icc.png")
        ok_button_color = "#28a745"  # Green
        sound_path = os.path.join(os.getcwd(), "sounds", "success.wav")
    elif message_type == "error":
        bg_image_path = os.path.join(os.getcwd(), "images", "error.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "eri.png")
        ok_button_color = "#dc3545"  # Red
        sound_path = os.path.join(os.getcwd(), "sounds", "error.wav")
    elif message_type == "warning":
        bg_image_path = os.path.join(os.getcwd(), "images", "warning.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "icw.png")
        ok_button_color = "#fd7e14"  # Orange
        sound_path = os.path.join(os.getcwd(), "sounds", "warning.wav")
    elif message_type == "win":
        bg_image_path = os.path.join(os.getcwd(), "images", "correct.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "check.png")
        ok_button_color = "#28a745"  # Green
        sound_path = None
    elif message_type == "lose":
        bg_image_path = os.path.join(os.getcwd(), "images", "wrong.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "no.png")
        ok_button_color = "#dc3545"  # Red
        sound_path = None

    elif message_type == "default":
        bg_image_path = os.path.join(os.getcwd(), "images", "default.png")
        icon_image_path = os.path.join(os.getcwd(), "images", "notification-bell.png")
        ok_button_color = "#6c757d"  # gray
        sound_path = None

    # Check SFX is not muted before play sounds
    if sound_path and not is_sfx_muted_state():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

    # background image
    bg_image = Image.open(bg_image_path).resize((450, 320), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(msg_box, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # icon image
    if icon_image_path:
        icon_image = Image.open(icon_image_path).resize((130, 130), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(icon_image)
        icon_label = Label(msg_box, image=icon_image)
        icon_label.place(relx=0.5, rely=0.45, anchor="center")
    else:
       
        pass

    message_label = Label(
        msg_box,
        text=message,
        font=("Futura", 14),
        fg="black",
        bg="#f6f6f6",
        wraplength=width - 40
    )
    message_label.place(relx=0.5, rely=0.7, anchor="center")

    #ok button
    def on_ok():
        global user_choice
        user_choice = True
        msg_box.destroy()
        
    #cancel button
    def on_cancel():
        global user_choice
        user_choice = False
        msg_box.destroy()

    if message_type == "warning":
        ok_button = Button(
            msg_box,
            text="OK",
            font=("Futura", 18),
            bg=ok_button_color,
            fg="white",
            command=on_ok,
            bd=0,
            highlightthickness=0,
            width=8,
            height=1,
            padx=15,
            pady=5
        )
        ok_button.place(relx=0.3, rely=0.85, anchor="center")

        cancel_button = Button(
            msg_box,
            text="Cancel",
            font=("Futura", 18),
            bg="#6c757d",  # Gray for cancel
            fg="white",
            command=on_cancel,
            bd=0,
            highlightthickness=0,
            width=8,
            height=1,
            padx=15,
            pady=5
        )
        cancel_button.place(relx=0.7, rely=0.85, anchor="center")
    else:
        # Default OK
        ok_button = Button(
            msg_box,
            text="OK",
            font=("Futura", 18),
            bg=ok_button_color,
            fg="white",
            command=on_ok,
            bd=0,
            highlightthickness=0,
            width=8,
            height=1,
            padx=15,
            pady=5
        )
        ok_button.place(relx=0.5, rely=0.85, anchor="center")


    msg_box.transient()
    msg_box.grab_set()
    msg_box.wait_window()

    return user_choice
