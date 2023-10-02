import io
import logging
import textwrap

from PIL import Image, ImageDraw, ImageFont

from models.image_task import SaveImageTask
from utils.redis_util import create_save_image_task


def add_rectangle(image, width, height):
    image = image.crop((0, 0, width, height + 100))
    pencil = ImageDraw.Draw(image)
    pencil.rectangle((0, height, width, height + height // 6), 'black')
    return image


def draw_line(pencil, offset, line, font, margin=2):
    pencil.text(
        (margin, offset),
        line,
        font=font,
        fill='white'
    )


def add_text_to_image(description, image, width, height, config):
    pencil = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    try:
        font = ImageFont.truetype(config['FONT'], size=config['FONT_SIZE'], encoding="utf-8")
    except OSError:
        logging.warning('Cannot load configured font, used default')
    offset = height
    line = ''
    words = description.split()
    for index, word in enumerate(description.split()):
        new_str = line
        if index != 0:
            new_str += ' '
        new_str += word

        (w_str, h_str), (_, _) = font.font.getsize(new_str)

        if w_str < width:
            line = new_str
        else:
            draw_line(pencil, offset, line, font)
            line = word
            offset += h_str + 5

        if index == len(words) - 1:
            draw_line(pencil, offset, line, font)

    return image


def handle_image(task, config, redis_conn):
    with Image.open(io.BytesIO(task.filedata)) as img:
        img.load()

    width, height = img.size

    try:
        img = add_rectangle(img, width, height)
    except Exception:
        logging.error(f'Cannot paint rectangle. Filetime = {task.time}')
        return
    try:
        img = add_text_to_image(task.description, img, width, height, config)
    except Exception:
        logging.error(f'Cannot print text. Filetime = {task.time}')
        return

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')

    create_save_image_task(redis_conn, SaveImageTask(
        description=task.description,
        filedata=img_byte_arr.getvalue(),
        time=task.time,
        filename=task.filename,
    ))
