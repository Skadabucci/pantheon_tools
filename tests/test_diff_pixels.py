from pantheon_tools.ExperiencePrediction import DARK_BLUE_COLOR
from PIL import Image

def diff_pixels(a, b):
    return sum((a - b) ** 2 for a, b in zip(a, b))

def test_diff_pixels():
    image_path = 'tests/data/variable_partial_exp_bar.png'
    image = Image.open(image_path)
    pixels = list(image.getdata())

    for pixel in pixels:
        diff = diff_pixels(pixel, DARK_BLUE_COLOR)
        print(f"{diff:<6} \033[48;2;{pixel[0]};{pixel[1]};{pixel[2]}m  \033[0m", end=' ')
        print(f"\033[48;2;{DARK_BLUE_COLOR[0]};{DARK_BLUE_COLOR[1]};{DARK_BLUE_COLOR[2]}m  \033[0m \n")

if __name__ == "__main__":
    test_diff_pixels()