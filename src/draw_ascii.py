import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from pathlib import Path


class ASCII_generate:
    def __init__(self, font_path, level, canvas_shape=(40, 40)):

        self.canvas = np.zeros(shape=canvas_shape) + 255
        self.font = ImageFont.truetype(font_path, size=10)
        self.printables = [chr(i) for i in range(32, 127)]
        self.level = level
        self.sort_brightness()
        self.generate_chars()

    def sort_brightness(self):
        brightnesses = np.zeros(len(self.printables))
        for i in range(len(self.printables)):
            img = Image.fromarray(self.canvas)
            draw = ImageDraw.Draw(img)
            draw.text(xy=(5, 5), text=self.printables[i], font=self.font)
            brightnesses[i] = np.mean(np.array(img))

        self.brightnesses_dict = dict()
        for i in range(len(brightnesses)):
            self.brightnesses_dict[self.printables[i]] = brightnesses[i]

        self.brightnesses_dict = dict(
            sorted(self.brightnesses_dict.items(), key=lambda item: item[1]))

    def generate_chars(self):
        ratios = [i/self.level for i in range(self.level)]
        quantiles = np.quantile(
            np.unique(list(self.brightnesses_dict.values())), ratios)
        final_chars = []
        for q in quantiles:
            final_chars.append(
                np.abs(list(self.brightnesses_dict.values()) - q).argmin())

        self.final_chars = [list(self.brightnesses_dict.keys())[
            i] for i in final_chars][::-1]

    def get_result(self):
        return self.final_chars


class DrawASCII:
    def __init__(self, ASCII_CHARS, output_size, alpha=1.1, beta=-25):

        self.ASCII_CHARS = ASCII_CHARS
        self.output_size = output_size
        self.alpha = alpha
        self.beta = beta

    def load_img_by_path(self, img_path):
        # if (img_path):
        self.image = cv2.imread(img_path)
        self.image = cv2.resize(self.image, self.output_size)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def load_img(self, img):
        self.image = img
        self.image = cv2.resize(self.image, self.output_size)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def map_px(self):
        ratio = 255/(len(self.ASCII_CHARS))
        converted = (self.image / ratio).astype(int)
        converted = np.clip(converted, 0, len(self.ASCII_CHARS) - 1)
        return np.array(self.ASCII_CHARS)[converted]


def main():

    level = 8
    output_size = (192, 58)
    # path = Path().cwd() / "pbui.jfif"
    # path = str(path)

    cap = cv2.VideoCapture("bad-apple.mp4")
    cap.set(1, 124)

    ret, im = cap.read()

    ascii_gen = ASCII_generate(font_path="ARIAL.TTF", level=level)
    ascii_gen.get_result()

    drawer = DrawASCII(ASCII_CHARS=ascii_gen.get_result(), output_size=output_size)
    drawer.load_img(im)

    res = drawer.map_px()

    print(res.shape)

    with open("result.txt", "w") as f:
        line = ""
        for l in res:
            line = "".join(l)+"\n"
            f.write(line)


if __name__ == "__main__":
    main()
