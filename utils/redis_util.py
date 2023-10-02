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
    if data_from_queue := conn.blpop(HANDLE_IMAGE_QUEUE, 60):
        return HandleImageTask.from_json(data_from_queue[1])
    return None


def create_save_image_task(conn, task: SaveImageTask):
    conn.rpush(SAVE_IMAGE_QUEUE, task.to_json())


def get_save_image_task(conn) -> SaveImageTask:
    if data_from_queue := conn.blpop(SAVE_IMAGE_QUEUE, 60):
        return SaveImageTask.from_json(data_from_queue[1])
    return None
