import pygame

pygame.mixer.init()

is_background_muted = False
is_sfx_muted = False

SOUND_FILES = {
    "click": "sounds/click.wav",
    "background": "sounds/background.wav",
    "win": "sounds/win.wav",
    "lose": "sounds/lose.wav",
    "timeover": "sounds/timeover.wav",
    "tile": "sounds/tile.wav",
    "game": "sounds/game.wav",
}
sounds = {name: pygame.mixer.Sound(path) for name, path in SOUND_FILES.items()}


def is_sfx_muted_state():
    return is_sfx_muted


def play_sound(sound_name):
    if sound_name in sounds and not is_sfx_muted:
        sounds[sound_name].play()


def play_background(loop=True):
    if "background" in sounds and not is_background_muted:
        sounds["background"].play(loops=-1 if loop else 0)


def stop_background():
    if "background" in sounds:
        sounds["background"].stop()

#Play background sound in gameplay
def play_game_sound(loop=True):
    global is_background_muted

    if not is_background_muted:
        is_background_muted = True
        stop_background()
        if "game" in sounds and not is_sfx_muted:
            sounds["game"].play(loops=-1 if loop else 0)

#Background sound mute function
def toggle_background_mute():

    global is_background_muted
    is_background_muted = not is_background_muted
    if is_background_muted:
        pygame.mixer.pause()
    else:
        pygame.mixer.unpause()
    return is_background_muted

#SFX sound mute function
def toggle_sfx_mute():
    global is_sfx_muted
    is_sfx_muted = not is_sfx_muted
    return is_sfx_muted


def play_win_sound():
    play_sound("win")


def play_lose_sound():
    play_sound("lose")


def play_tile_sound():
    play_sound("tile")


def play_timeover_sound():
    play_sound("timeover")