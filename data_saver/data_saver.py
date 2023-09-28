import io
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
    try:
        image.save(path_to_file)
        print(path_to_file)
    except Exception as e:
        print(e)
    return path_to_file


def save_image(task, cf):
    path = save_image_to_file(task.filedata, cf)
    with Session() as session:
        photo = session.add(ImageEntity(
            description=task.description,
            filepath=path,
            time=datetime.fromtimestamp(task.time),
        ))
        session.commit()
