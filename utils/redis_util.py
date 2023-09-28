import redis

from models.image_task import HandleImageTask, SaveImageTask

HANDLE_IMAGE_QUEUE = 'handle_images_queue'
SAVE_IMAGE_QUEUE = 'save_images_queue'


def init_redis(config):
    conn = redis.Redis(
        host=config['HOST'],
        port=config['PORT'],
        db=config['DB_NUM'],
        password=config['PASS'],
    )
    conn.ping()
    return conn


def create_handle_image_task(conn, task: HandleImageTask):
    conn.rpush(HANDLE_IMAGE_QUEUE, task.to_json())


def get_handle_image_task(conn) -> HandleImageTask:
    return HandleImageTask.from_json(conn.lpop(HANDLE_IMAGE_QUEUE))


def create_save_image_task(conn, task: SaveImageTask):
    conn.rpush(SAVE_IMAGE_QUEUE, task.to_json())


def get_save_image_task(conn) -> SaveImageTask:
    return SaveImageTask.from_json(conn.lpop(SAVE_IMAGE_QUEUE))
