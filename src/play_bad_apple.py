import os
import time
import pygame
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
# Old version, running from bad-apple.txt

if __name__ == "__main__":

    p = Path(__file__).parent.parent
    music_path = str(p / "data/bad-apple.mp3")
    txt_path = str(p / "bad-apple.txt")
    # print(Path(__file__).parent)
    pygame.mixer.init()
    os.system("cls")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.15)
    FPS = int(os.getenv("FPS"))

    ascii_art_height = int(os.getenv("ASCII_OUTPUT_HEIGHT"))
    print("===============Do NOT change your CMD window size ples!============")
    time.sleep(1)

    with open(txt_path, "r") as f:
        lines = f.readlines()
        lines = [line.replace("\n", "").replace(" ",".") for line in lines]

    pygame.mixer.music.play(start=0.28)
    # time.sleep(0.005)
    start = 0
    for i in range(ascii_art_height, len(lines), ascii_art_height):
        print_lines = ""
        for j in range(start, i):
            # print(lines[j])
            print_lines = print_lines + lines[j] + "\n"

        print(print_lines)
        time.sleep(1/FPS)
        # time.sleep(0.03332318)
        start = i
        # os.system("cls")
        print("\r", end="", flush=True)

    pygame.mixer.music.stop()




            
