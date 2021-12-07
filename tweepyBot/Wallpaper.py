import os
from PIL import Image, ImageDraw
import textwrap


def get_wallpaper(url):
    os.system("curl " + url + " > cat.jpg")

    # 저장 된 이미지 확인
    img = Image.open("cat.jpg")
    img.save('created_image.png')
    print("create Image")


def draw_text_on_image(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height
