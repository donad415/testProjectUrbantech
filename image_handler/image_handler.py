import io
import textwrap

from PIL import Image, ImageDraw, ImageFont

from models.image_task import SaveImageTask
from utils.redis_util import create_save_image_task


def add_rectangle(image, width, height):
    image = image.crop((0, 0, width, height + 100))
    pencil = ImageDraw.Draw(image)
    pencil.rectangle((0, height, width, height + height // 6), 'black')
    return image


def add_text_to_image(image, width, height, config):
    pencil = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    try:
        font = ImageFont.truetype(config['FONT'], size=20)
    except OSError as e:
        print(e)
    margin = 0
    offset = height
    for line in textwrap.wrap(task.description, width=width // 7):
        pencil.text(
            (margin, offset),
            line,
            font=font,
            fill='white'
        )
        offset += 25
    return image


def handle_image(task, config, redis_conn):
    with Image.open(io.BytesIO(task.filedata)) as img:
        img.load()

    width, height = img.size

    img = add_rectangle(img, width, height)
    img = add_text_to_image(img, width, height, config)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')

    create_save_image_task(redis_conn, SaveImageTask(
        description=task.description,
        filedata=img_byte_arr.getvalue(),
        time=task.time,
        filename=task.filename,
    ))
