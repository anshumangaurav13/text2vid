from PIL import Image, ImageDraw, ImageFont
import os
import subprocess


def import_txt_as_list(file_path):
    word_list = [" ", " "]
    with open(file_path, "r") as file:
        content = file.read()
        line_list = content.split("\n")
        word_list = []
        for line in line_list:
            words = line.split()
            for w in words:
                word_list.append(w)
                if w[-1] == "." or w[-1] == ",":
                    word_list.append(" ")
            word_list.append(" ")
    return word_list


def create_empty_image(width=600, height=150, background_color=(255, 255, 255)):
    return Image.new("RGB", (width, height), background_color)


def add_text_to_image(
    image,
    text,
    text_color=(0, 0, 0),
    font_size=48,
    font_path="samplefont.ttf",
):
    draw = ImageDraw.Draw(image)
    w, h = get_text_size(text)
    if w > image.width:
        font_size //= 2
        w //= 2
        h //= 2
    font = ImageFont.truetype(font_path, font_size) if font_path else None
    position = (image.width / 2 - w / 2, image.height / 2 - h)
    draw.text(position, text, fill=text_color, font=font)


def save_image(image, file_path):
    image.save(file_path)


def get_text_size(text, font_path="samplefont.ttf", font_size=48):
    font = ImageFont.truetype(font_path, font_size)
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom - top


def create_video_from_images(output_path, output_format="mp4", fps=4):
    ffmpeg_command = [
        "ffmpeg",
        "-framerate",
        str(fps),
        "-i",
        os.path.join(
            "imgs", "%d.png"
        ),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-y",  # Overwrite output file if it exists
        output_path,
    ]

    subprocess.run(ffmpeg_command)


file_path = input("Enter file name: ")
result_list = import_txt_as_list(file_path)
print(result_list)
os.makedirs("imgs", exist_ok=True)
for i, word in enumerate(result_list):
    img = create_empty_image()
    add_text_to_image(img, word)
    save_image(img, f"imgs/{i}.png")

create_video_from_images("out.mp4")