from tkinter import *
from PIL import Image, ImageTk
from database import  update_user_info, delete_user
from message import custom_message_box
from sound import play_sound
import sqlite3

def on_click():
    play_sound("click")

#Edit user details 
def toggle_edit(entry_field, edit_button, current_value, username, field_name):
    if edit_button["image"] == str(edit_image):
        edit_button.config(image=save_image)
        entry_field.config(state=NORMAL)
    else:
        new_value = entry_field.get()
        if new_value == current_value:
            custom_message_box("No changes were made.", "default")
        else:
            try:
                update_user_info(username, field_name, new_value)
                custom_message_box(f"{field_name.capitalize()} updated successfully!", "success")
            except sqlite3.Error as e:
                custom_message_box(f"Error updating {field_name}: {e}", "error")
        entry_field.config(state=DISABLED)
        edit_button.config(image=edit_image)

#Delete account 
def delete_account(username, root):
    confirm = custom_message_box("Are you sure you want to delete your account?", "warning")
    if confirm:
        try:
            delete_user(username)
            custom_message_box("Your account has been deleted.", "success")
            root.destroy()
        except sqlite3.Error as e:
            custom_message_box(f"Error deleting account: {e}", "error")

#Show placeholder in text fields
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def open_profile(username, password):
    profile = Toplevel()
    profile.state('zoomed')
    profile.geometry('1366x768+0+0')
    profile.title("Profile")
    profile.iconbitmap("icon.ico")

    global edit_image, save_image, delete_image, AppBg
    try:
        edit_image = ImageTk.PhotoImage(Image.open('images/editbtn.png').resize((210, 75), Image.LANCZOS))
        save_image = ImageTk.PhotoImage(Image.open('images/save.png').resize((210, 75), Image.LANCZOS))
        delete_image = ImageTk.PhotoImage(Image.open('images/deletebbtn.png').resize((550, 80), Image.LANCZOS))
        bg_image = Image.open('images/profile.png').resize((1366, 730), Image.LANCZOS)
        AppBg = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        profile.destroy()
        return

    background_label = Label(profile, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Username field
    username_entry = Entry(profile, font=("Arial", 25))
    username_entry.place(x=370, y=250, width=400)
    if username:
        username_entry.insert(0, username)
    else:
        add_placeholder(username_entry, "Enter your username")

    username_edit_button = Button(profile, image=edit_image, bd=0, highlightthickness=0, compound=LEFT,
                                  command=lambda: [on_click(), toggle_edit(username_entry, username_edit_button, username,
                                                                           username, "username")])
    username_edit_button.place(x=830, y=230)

    # Password field
    password_entry = Entry(profile, font=("Arial", 25), show="*")
    password_entry.place(x=370, y=360, width=400)
    if password:
        password_entry.insert(0, password)
    else:
        add_placeholder(password_entry, "Enter your password")

    password_edit_button = Button(profile, image=edit_image, bd=0, highlightthickness=0, compound=LEFT,
                                  command=lambda: [on_click(), toggle_edit(password_entry, password_edit_button, password,username, "password")])
    password_edit_button.place(x=830, y=343)

    #Delete account button
    delete_button = Button(profile, image=delete_image, bd=0, highlightthickness=0,command=lambda: [on_click(), delete_account(username, profile)])
    delete_button.place(x=700, y=610, anchor=CENTER)

    profile.mainloop()
