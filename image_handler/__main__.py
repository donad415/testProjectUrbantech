import logging
import os
import sys

from image_handler import handle_image
from utils.redis_util import init_redis, get_handle_image_task
from utils.yaml_reader import read_yaml

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )

    cf = read_yaml(os.getenv('CONFIG_PATH', '../config.yaml'))
    redis_conn = init_redis(cf['REDIS'])

    logging.info('image_handler was successfully started')

    while True:
        task = None
        try:
            task = get_handle_image_task(redis_conn)
        except Exception as e:
            logging.error(f'Cannot parse task from queue. Exception: {e}')
        if task:
            try:
                handle_image(task, cf, redis_conn)
            except Exception as e:
                logging.error(f'Cannot handle image. Filetime:{task.time} Exception: {e}')
