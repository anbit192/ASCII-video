
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from pathlib import Path

# Color draw_ascii functions


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
        ratios.append(1)
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


def map_rgb_to_ansi(r, g, b):
    return f"\x1B[38;2;{r};{g};{b}m"


class DrawASCII:
    def __init__(self, output_size, color=True, ASCII_CHARS=[]):

        self.ASCII_CHARS = ASCII_CHARS
        self.output_size = output_size
        self.color = color

    def load_img_by_path(self, img_path):
        # if (img_path):
        self.image = cv2.imread(img_path)
        self.image = cv2.resize(self.image, self.output_size)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def load_img(self, img):
        self.image = img
        self.image = cv2.resize(self.image, self.output_size)
        # self.image = cv2.convertScaleAbs(self.image, alpha=self.alpha, beta=self.beta)

    def map_px(self):
        ratio = 255/(len(self.ASCII_CHARS))
        converted = (self.image[:, :, 0] / ratio).astype(int)
        converted = np.clip(converted, 0, len(self.ASCII_CHARS) - 1)
        return np.array(self.ASCII_CHARS)[converted]

    def color_px(self):
        return np.array([f"{map_rgb_to_ansi(r, g, b)}@" for b, g, r in self.image.reshape((-1, 3))]).reshape((self.output_size[::-1]))

    def get_result(self):
        if (self.color == False):
            ascii_chars = self.map_px()
            return ascii_chars

        elif (self.color == True):
            color_map = self.color_px()
            # concat = np.char.add(color_map, ascii_chars)
            return color_map
