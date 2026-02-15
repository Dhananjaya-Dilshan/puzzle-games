from tkinter import *
from PIL import Image, ImageTk
from leaderbord import open_leaderboard
from signup import open_signup_page
from login import open_login_page
from sound import toggle_background_mute, toggle_sfx_mute, play_sound, play_background


play_background()

def on_click():
    play_sound("click")

root = Tk()
root.state('zoomed')
root.geometry('1366x768+0+0')
root.title("Puzzel game")
root.iconbitmap("icon.ico")

# Background image
bg_image = Image.open('images/bg.png').resize((1366, 750), Image.Resampling.LANCZOS)
AppBg = ImageTk.PhotoImage(bg_image)
background_label = Label(root, image=AppBg, bd=0, highlightthickness=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Toggle sound icons
mute_bg_image = ImageTk.PhotoImage(Image.open('images/mute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
unmute_bg_image = ImageTk.PhotoImage(Image.open('images/unmute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
mute_sfx_image = ImageTk.PhotoImage(Image.open('images/mute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
unmute_sfx_image = ImageTk.PhotoImage(Image.open('images/unmute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))

def toggle_background_button():
    global is_bg_muted
    is_bg_muted = toggle_background_mute()
    bg_mute_button.config(image=(mute_bg_image if is_bg_muted else unmute_bg_image))

bg_mute_button = Button(root, image=unmute_bg_image, bd=0, highlightthickness=0, command=toggle_background_button)
bg_mute_button.place(x=1250, y=50)

# SFX Button
is_sfx_muted = False
def toggle_sfx_button():
    global is_sfx_muted
    is_sfx_muted = toggle_sfx_mute()
    sfx_mute_button.config(image=(mute_sfx_image if is_sfx_muted else unmute_sfx_image))

sfx_mute_button = Button(root, image=unmute_sfx_image, bd=0, highlightthickness=0, command=toggle_sfx_button)
sfx_mute_button.place(x=1180, y=50)

p_image = Image.open('images/pgame.png').resize((700, 200), Image.Resampling.LANCZOS)
p_btn = ImageTk.PhotoImage(p_image)
p_button = Button(root, image=p_btn, bd=0, highlightthickness=0)
p_button.place(x=310, y=50)


# Sign-up
signup_image = Image.open('images/signup.png').resize((300, 80), Image.Resampling.LANCZOS)
signup_btn = ImageTk.PhotoImage(signup_image)
signup_button = Button(root, image=signup_btn, bd=0, highlightthickness=0, command=lambda: [on_click(), open_signup_page(root)])
signup_button.place(x=530, y=210)

# Play
play_image = Image.open('images/play.png').resize((400, 120), Image.Resampling.LANCZOS)
play_btn = ImageTk.PhotoImage(play_image)
play_button = Button(root, image=play_btn, bd=0, highlightthickness=0, command=lambda: [on_click(), open_login_page(root)])
play_button.place(x=480, y=340)

# Leaderboard
leaderboard_image = Image.open('images/leader.png').resize((150, 150), Image.Resampling.LANCZOS)
leaderboard_btn = ImageTk.PhotoImage(leaderboard_image)
leaderboard_button = Button(root, image=leaderboard_btn, bd=0, highlightthickness=0, command=lambda: [on_click(), open_leaderboard()])
leaderboard_button.place(x=600, y=500)

root.mainloop()