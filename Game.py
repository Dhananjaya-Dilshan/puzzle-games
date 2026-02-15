from tkinter import *
from PIL import Image, ImageTk
import os
from random import shuffle
import requests
from io import BytesIO
from message import custom_message_box
from sound import *
from database import get_user_level, update_user_level, update_best_time


def on_click():
    play_sound("click")


remaining_stars = 3
time_limit = 300
paused = False

def update_timer():
    global time_limit, paused
    if not paused:
        minutes = time_limit // 60
        seconds = time_limit % 60
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        if time_limit > 0:
            time_limit -= 1
            Game.after(1000, update_timer)
        else:
            custom_message_box("The Time is over!", "default")
            play_timeover_sound()
            Game.destroy()


def get_more_time():
    global remaining_stars, paused, time_limit
    if remaining_stars > 0:
        paused = True
        remaining_stars -= 1
        update_stars()
        open_time(Game, resume_timer)


def resume_timer(additional_time=60):
    global paused, time_limit
    paused = False
    time_limit += additional_time
    update_timer()


def update_stars():
    stars_label.config(text="★" * remaining_stars + "" * (3 - remaining_stars))


def open_Game(category, username):
    global Game, lt, ltc, Lab, index, timer_label, stars_label, filename_label

    Game = Toplevel()
    Game.state('zoomed')
    Game.geometry('1366x768+50+50')
    Game.title(f"{category.capitalize()} Puzzle")
    Game.iconbitmap("icon.ico")

    play_game_sound()

    bg_image = Image.open('images/gamsdsdse.png').resize((1366, 730), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(Game, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    Game.bg_image = AppBg

    # Toggle sound icons
    mute_bg_image = ImageTk.PhotoImage(Image.open('images/mute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    unmute_bg_image = ImageTk.PhotoImage(Image.open('images/unmute_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    mute_sfx_image = ImageTk.PhotoImage(Image.open('images/mute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))
    unmute_sfx_image = ImageTk.PhotoImage(Image.open('images/unmute_sfx_icon.png').resize((60, 60), Image.Resampling.LANCZOS))

    def toggle_background_button():
        global is_bg_muted
        is_bg_muted = toggle_background_mute()
        bg_mute_button.config(image=(mute_bg_image if is_bg_muted else unmute_bg_image))

    bg_mute_button = Button( Game, image=unmute_bg_image, bd=0, highlightthickness=0,command=toggle_background_button)
    bg_mute_button.place(x=160, y=60)

    # SFX Toggle Button
    is_sfx_muted = False

    def toggle_sfx_button():
        global is_sfx_muted
        is_sfx_muted = toggle_sfx_mute()
        sfx_mute_button.config(image=(mute_sfx_image if is_sfx_muted else unmute_sfx_image))

    sfx_mute_button = Button( Game, image=unmute_sfx_image, bd=0, highlightthickness=0, command=toggle_sfx_button)
    sfx_mute_button.place(x=80, y=60)

    timer_image = Image.open('images/timer bg.png').resize((200, 80), Image.Resampling.LANCZOS)
    timer_photo = ImageTk.PhotoImage(timer_image)
    timer_label = Label(Game, image=timer_photo, bd=0)
    timer_label.place(x=1060, y=45)
    Game.timer_photo = timer_photo

    timer_label = Label(Game, text="03:00", font=("Arial", 36), bg="#005a98", fg="white")
    timer_label.place(x=1100, y=50)

    stars_label = Label(Game, text="★★★", font=("Arial", 40), bg="#f8d341", fg="green")
    stars_label.place(x=1080, y=320)

    time_button_image = Image.open('images/time.png').resize((300, 110), Image.Resampling.LANCZOS)
    time_button_photo = ImageTk.PhotoImage(time_button_image)
    more_time_button = Button(Game, image=time_button_photo, bd=0, highlightthickness=0,command=lambda: [on_click(), get_more_time()])
    more_time_button.place(x=1020, y=200)

    Game.time_button_photo = time_button_photo

    current_level = get_user_level(username, category)
    if current_level >= 10:

        custom_message_box(f"You've completed all levels in the {category} category!", "default")
        return

    image_path = f'Images/{category}'
    image_files = sorted(os.listdir(image_path))
    selected_image = os.path.join(image_path, image_files[current_level])

    leve_label = Label(Game, text=f"Level {current_level + 1}", font=("Futura", 30, "bold"), fg="black", bg="#f8d343")
    leve_label.place(x=530, y=650)

    sample_image = Image.open(selected_image).resize((250, 250), Image.Resampling.LANCZOS)
    sample_image_photo = ImageTk.PhotoImage(sample_image)
    sample_label = Label(Game, image=sample_image_photo, bd=0, highlightthickness=0)
    sample_label.place(x=1050, y=420)
    Game.sample_image_photo = sample_image_photo

    # Code snippet inspired by https://youtu.be/hGHwW6Xd2gg?si=YvCTAtfQbAR9QDg9
    lt, ltc, Lab = [], [], []
    frame = Frame(Game, bg="#000")
    frame.place(x=315, y=30, width=600, height=600)

    cmp = 0
    for i in range(3):
        for j in range(3):
            tile_frame = Frame(frame, bg="#000")
            if i == 2 and j == 2:
                lt.append(["", cmp])
                ltc.append(["", cmp])
                Lab.append(Label(tile_frame, background="#faf5f5"))
            else:
                img = Image.open(selected_image).resize((600, 600)).crop(
                    ((j * 200), (i * 200), (j + 1) * 200, (i + 1) * 200)
                )
                img = ImageTk.PhotoImage(img)
                lt.append([img, cmp])
                ltc.append([img, cmp])
                Lab.append(Label(tile_frame, image=img, background="#faf5f5"))

            Lab[cmp].bind("<Button-1>", lambda event, h=cmp: tile_click(event, h))
            Lab[cmp].place(x=2, y=2, width=196, height=196)
            tile_frame.place(x=j * 200, y=i * 200, width=200, height=200)
            cmp += 1

    shuffle_tiles()
    update_timer()
    Game.mainloop()


#API finction for get more time
def open_time( Game,resume_callback):
    try:
        response = requests.get("http://marcconrad.com/uob/banana/api.php")
        data = response.json()
        question_url = data["question"]
        solution = str(data["solution"])
    except Exception as e:
        print("Error fetching data from API:", e)
        return


    time_win = Toplevel(Game)
    time_win.geometry('1000x700+160+0')
    time_win.title("Time Window")
    time_win.overrideredirect(True)

    bg_image = Image.open('images/api.png')
    bg_image = bg_image.resize((1000, 700), Image.Resampling.LANCZOS)
    AppBg = ImageTk.PhotoImage(bg_image)
    background_label = Label(time_win, image=AppBg, bd=0, highlightthickness=0)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    time_win.bg_image = AppBg

    # Load question
    try:
        img_response = requests.get(question_url)
        img_data = Image.open(BytesIO(img_response.content))
        img_data = img_data.resize((600, 400), Image.Resampling.LANCZOS)
        question_img = ImageTk.PhotoImage(img_data)
        question_label = Label(time_win, image=question_img, bd=0)
        question_label.place(x=200, y=150)
        time_win.question_img = question_img
    except Exception as e:
        print("Error loading question image:", e)
        return

    # Entry answer
    entry_answer = Entry(time_win, font=("Arial", 18))
    entry_answer.place(x=300, y=620)


    def check_answer():
        user_answer = entry_answer.get()
        if user_answer == solution:
            play_win_sound()
            custom_message_box("Your answer is Correct!", "win")
            resume_callback()  # Add time
        else:
            play_lose_sound()
            custom_message_box("Your answer is Wrong.", "lose")
            resume_callback(0)  # No extra time added

        Game.deiconify()  # Show Game window
        time_win.destroy()  # Close time window

    # Enter button
    enter_image = Image.open('images/enter.png')
    enter_image = enter_image.resize((150, 60), Image.Resampling.LANCZOS)
    enter_btn_img = ImageTk.PhotoImage(enter_image)
    enter_button = Button(time_win, image=enter_btn_img, bd=0, highlightthickness=0, command=lambda:[on_click(),check_answer()])
    enter_button.place(x=580, y=610)
    time_win.enter_btn_img = enter_btn_img

    time_win.mainloop()
    
# Code snippet inspired by https://youtu.be/hGHwW6Xd2gg?si=YvCTAtfQbAR9QDg9
def shuffle_tiles():
    global ltc, Lab, index
    shuffle(ltc)
    for i, label in enumerate(Lab):
        label.config(image=ltc[i][0])
        label.config(bg="#3b53a0" if ltc[i][0] else "#242424")
        if not ltc[i][0]:  # Empty tile
            index = i

 # Code snippet inspired by https://youtu.be/hGHwW6Xd2gg?si=YvCTAtfQbAR9QDg9
def tile_click(event, tile_index):
    global index, Lab, lt, ltc

    # check if the clicked tile is adjacent to the empty tile
    adjacent_indices = [index - 1, index + 1, index - 3, index + 3]
    if tile_index in adjacent_indices:
        # Swap the clicked tile with the empty tile
        play_tile_sound()
        Lab[index].config(image=ltc[tile_index][0], bg="#3b53a0")
        Lab[tile_index].config(image="", bg="#242424")

        # Update representation of the tiles
        ltc[index], ltc[tile_index] = ltc[tile_index], ltc[index]

        # Update the empty tile index
        index = tile_index

        # Check if the puzzle is complete
        if check_puzzle_complete():
            display_win_message()

 # Code snippet inspired by https://youtu.be/hGHwW6Xd2gg?si=YvCTAtfQbAR9QDg9
def check_puzzle_complete():

    for i in range(len(ltc)):
        if ltc[i][1] != lt[i][1]:
            return False
    return True


def display_win_message(username, category):
    global Game, current_level, time_limit

    elapsed_time = 300 - time_limit
    update_best_time(username, category, elapsed_time)

    win_label = Label(Game, text="You Win!", font=("Helvetica", 24), bg="#3b53a0", fg="white")
    win_label.place(x=300, y=650, width=200, height=50)

    # Increment level
    next_level = get_user_level(username, category) + 1
    if next_level < 10:
        update_user_level(username, category, next_level)
        custom_message_box(f"Level {next_level} unlocked!", "default")
    else:
        custom_message_box(f"You've completed all levels in the {category} category!", "default")
        update_user_level(username, category, 0)  # Reset level

    Game.destroy()



