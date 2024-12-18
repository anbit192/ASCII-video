import time
import os
import cv2
from dotenv import load_dotenv
from pathlib import Path
import threading
import pygame
import sys
from draw_ascii import *
from moviepy.editor import VideoFileClip

# New version, generate ASCII and display its frames in real time

load_dotenv()
ASCII_LEVEL=int(os.getenv("ASCII_LEVEL"))
ASCII_OUTPUT_WIDTH=int(os.getenv("ASCII_OUTPUT_WIDTH"))
ASCII_OUTPUT_HEIGHT=int(os.getenv("ASCII_OUTPUT_HEIGHT"))
# FPS = int(os.getenv("FPS"))
VIDEO_NAME = os.getenv("VIDEO_NAME")

def play_music():
    pygame.mixer.music.play()


def main():
    no_audio_flag = False
    p = Path(__file__).parent.parent
    font_p = str(p / "data/ARIAL.TTF")
    video_p = str(p / "data" / VIDEO_NAME)
    split_name = VIDEO_NAME.split(".")[0]

    mp4_file = video_p
    mp3_file = p / "data" / f"{split_name}.mp3"

    if (mp3_file.is_file() == False):

        video_clip = VideoFileClip(mp4_file)
        audio_clip = video_clip.audio
        if (audio_clip is None):
            no_audio_flag = True
            print("Video has no audio.")
        else:
            no_audio_flag = False
            audio_clip.write_audiofile(mp3_file)

            audio_clip.close()
            video_clip.close()

    if (no_audio_flag == False):
        music_path = str(mp3_file)

        pygame.mixer.init()
        os.system("cls")
        pygame.mixer.music.load(music_path)

        vol = input("Set volume level (0 - 1) (Default: 0.5):\n")
        if not vol.strip():
            vol = 0.5
        else:
            vol = float(vol)

        pygame.mixer.music.set_volume(vol)

    cap = cv2.VideoCapture(video_p)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    print("Enable color? (0/1):\n")
    color = int(input())

    if (color == 0):
        ascii_gen = ASCII_generate(font_path=font_p, level=ASCII_LEVEL)
        chars = ascii_gen.get_result()
        drawer = DrawASCII(ASCII_CHARS=chars, output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT), color=(1==color))
    else:
        drawer = DrawASCII(output_size=(ASCII_OUTPUT_WIDTH, ASCII_OUTPUT_HEIGHT), color=(1==color))

    if (no_audio_flag == False):
        music_thread = threading.Thread(target=play_music)
        music_thread.start()

    ulti_start = time.perf_counter()

    while cap.isOpened():
        ret, frame = cap.read()
        curr = time.perf_counter() - ulti_start
        
        if not ret:
            break
        
        target_frame = int(curr * FPS)
        actual_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        if actual_frame < target_frame: # Frame skip babe!
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            continue

        drawer.load_img(img=frame)

        res = drawer.get_result()


        temp = "\n".join("".join(line) for line in res)
        sys.stdout.write("\x1B[H" +temp)

        # end_time = time.time()

        # process_time = end_time - start_time

        # if (process_time < frame_duration): # Just in case the frame is slower than the delay
        #     time.sleep(frame_duration - process_time)

        sys.stdout.write(f"\n\x1B[0mExpected Frame: \x1B[32m{target_frame}\x1B[0m, Actual Frame: \x1B[32m{actual_frame}\x1B[0m")

        
    sys.stdout.write("\x1B[0m")

    cap.release()

if __name__ == "__main__":
    main()
