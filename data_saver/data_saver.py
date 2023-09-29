import io
import logging
import os.path
import random
import string
from datetime import datetime

from PIL import Image

from utils.db_util import Session, ImageEntity


def save_image_to_file(image_bytes, config):
    image = Image.open(io.BytesIO(image_bytes))
    characters = string.ascii_letters + string.digits

    folder = ''.join(random.choice(characters) for _ in range(10))
    path_to_dir = os.path.join(config['UPLOAD_FILE_DIR'], folder)
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)

    filename = ''.join(random.choice(characters) for _ in range(10)) + f'.{image.format}'
    path_to_file = os.path.join(path_to_dir, filename)

    image.save(path_to_file)
    return path_to_file


def save_image(task, cf):
    try:
        path = save_image_to_file(task.filedata, cf)
    except Exception as e:
        logging.error(f'Cannot save image file. Filetime: {task.time} Exception: {e}')
        return
    with Session() as session:
        try:
            session.add(ImageEntity(
                description=task.description,
                filepath=path,
                time=datetime.fromtimestamp(task.time),
            ))
            session.commit()
        except Exception as e:
            logging.error(f'Cannot save image info to database. Filetime: {task.time} Exception: {e}')
