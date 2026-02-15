from tkinter import *
from PIL import Image, ImageTk
from database import get_leaderboard_data

def open_leaderboard():
    leaderboard = Toplevel()
    leaderboard.state('zoomed')
    leaderboard.geometry('1366x768+0+0')
    leaderboard.title("Leaderboard")


    bg_image = Image.open('images/leaderbord.png')
    bg_image = bg_image.resize((1366, 750), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(leaderboard, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    line_bg_image = Image.open('images/leardib.png')
    line_bg_image = line_bg_image.resize((1100, 80), Image.Resampling.LANCZOS)
    line_bg = ImageTk.PhotoImage(line_bg_image)

     # Define distances method using generative AI
    initial_y_line = 180
    initial_y_text = 190
    line_spacing = 105
    position_x_offset = 300
    username_x_offset = 600
    best_time_x_offset = 1000

    # leaderboard data
    leaderboard_data = get_leaderboard_data()

    # Display leaderboard method using generative AI
    for i, (username, best_time) in enumerate(leaderboard_data):
        y_position_line = initial_y_line + i * line_spacing
        y_position_text = initial_y_text + i * line_spacing


        line_label = Label(leaderboard, image=line_bg, bd=0)
        line_label.place(x=150, y=y_position_line)


        position_label = Label(leaderboard, text=f"{i + 1}", font=("Futura", 35, "bold"), bg="#259902", fg="white")
        position_label.place(x=position_x_offset, y=y_position_text)


        username_label = Label(leaderboard, text=username, font=("Futura", 30), bg="#259902", fg="white")
        username_label.place(x=username_x_offset, y=y_position_text)


        best_time_label = Label(leaderboard, text=f"{best_time:.2f}", font=("Futura", 30), bg="#259902", fg="white")
        best_time_label.place(x=best_time_x_offset, y=y_position_text)

    leaderboard.mainloop()
