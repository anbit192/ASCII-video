import os
import time

if __name__ == "__main__":
    ascii_art_height = 58
    print("===============Do NOT change your CMD window size ples!============")
    time.sleep(1)
    print("Starting after 5 seconds....")
    for i in range(1, 6):
        print(f"\r{i}", end="", flush=True)
        time.sleep(1)

    with open("bad-apple.txt", "r") as f:
        lines = f.readlines()
        lines = [line.replace("\n", "") for line in lines]
        
    start = 0
    for i in range(ascii_art_height, len(lines), ascii_art_height):
        print_lines = ""
        for j in range(start, i):
            # print(lines[j])
            print_lines = print_lines + lines[j] + "\n"

        print(print_lines)
        time.sleep(1/45)
        start = i
        # os.system("cls")
        print("\r", end="", flush=True)




            
