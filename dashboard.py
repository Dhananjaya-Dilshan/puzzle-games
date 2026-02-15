from tkinter import *
from PIL import Image, ImageTk
from Profile import open_profile
from category import open_category
from database import get_user_best_time
from leaderbord import open_leaderboard
from sound import toggle_background_mute, toggle_sfx_mute, play_sound

def on_click():
    # Play click sound
    play_sound("click")

def logout(root):
    root.destroy()

def open_dashboard(username,password):

    Dashboard = Toplevel()
    Dashboard.state('zoomed')
    Dashboard.geometry('1366x768+0+0')
    Dashboard.title("Dashboard")



    bg_image = Image.open('images/Dashbord .png')
    bg_image = bg_image.resize((1366, 750), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(Dashboard, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Toggle icons
    mute_bg_image = ImageTk.PhotoImage(Image.open('images/mute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    unmute_bg_image = ImageTk.PhotoImage(Image.open('images/unmute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    mute_sfx_image = ImageTk.PhotoImage(Image.open('images/mute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    unmute_sfx_image = ImageTk.PhotoImage(Image.open('images/unmute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))

    def toggle_background_button():
        global is_bg_muted
        is_bg_muted = toggle_background_mute()
        bg_mute_button.config(image=(mute_bg_image if is_bg_muted else unmute_bg_image))

    bg_mute_button = Button(Dashboard, image=unmute_bg_image, bd=0, highlightthickness=0, command=toggle_background_button)
    bg_mute_button.place(x=1250, y=50)

    # SFX Toggle Button
    is_sfx_muted = False
    def toggle_sfx_button():
        global is_sfx_muted
        is_sfx_muted = toggle_sfx_mute()
        sfx_mute_button.config(image=(mute_sfx_image if is_sfx_muted else unmute_sfx_image))

    sfx_mute_button = Button(Dashboard, image=unmute_sfx_image, bd=0, highlightthickness=0, command=toggle_sfx_button)
    sfx_mute_button.place(x=1180, y=50)

    # welcome message
    welcome_label = Label(Dashboard,
                          text=f"Welcome,\n{username}!",
                          font=("Futura",65, "bold"),
                          fg="#196e04",
                          bg="#fed52d")
    welcome_label.place(relx=0.5, y=180, anchor="center")

    # best time 
    best_time = get_user_best_time(username)
    best_time_label = Label(Dashboard,
                            text=f"Best Time\n {best_time} sec",
                            font=("Futura", 30, "bold"),
                            fg="#196e04",
                            bg="#fed52d")
    best_time_label.place(x=1070, y=125)

    # Profile
    profile_image = Image.open('images/Profilebtn.png')
    profile_image = profile_image.resize((300, 80), Image.Resampling.LANCZOS)
    profile_btn = ImageTk.PhotoImage(profile_image)
    profile_button = Button(Dashboard, image=profile_btn, bd=0, highlightthickness=0,command=lambda:  [on_click(),open_profile(username,password)])
    profile_button.place(x=1020, y=250)

    # Play
    pplay_image = Image.open('images/play.png')
    pplay_image = pplay_image.resize((400, 120), Image.Resampling.LANCZOS)
    pplay_btn = ImageTk.PhotoImage(pplay_image)
    pplay_button = Button(Dashboard, image=pplay_btn, bd=0, highlightthickness=0, command=lambda: [on_click(),open_category(Dashboard, username)])
    pplay_button.place(x=500, y=400)

    #leaderboard
    leaderboard_image = Image.open('images/leader.png')
    leaderboard_image = leaderboard_image.resize((150, 150), Image.Resampling.LANCZOS)
    leaderboard_btn = ImageTk.PhotoImage(leaderboard_image)
    leaderboard_button = Button(Dashboard, image=leaderboard_btn, bd=0,highlightthickness=0, command=lambda: [on_click(),open_leaderboard()])
    leaderboard_button.place(x=1100, y=400)

    # Logout
    logout_image = Image.open('images/logoutbtn.png')
    logout_image = logout_image.resize((300, 80), Image.Resampling.LANCZOS)
    logout_btn = ImageTk.PhotoImage(logout_image)
    logout_button = Button(Dashboard, image=logout_btn, bd=0, highlightthickness=0, command=lambda: [on_click(),logout(Dashboard)])
    logout_button.place(x=1020, y=600)


    Dashboard.mainloop()