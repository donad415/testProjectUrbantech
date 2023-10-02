import logging
import os
import sys

from data_saver import save_image
from utils.redis_util import init_redis, get_save_image_task
from utils.yaml_reader import read_yaml

if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )

    cf = read_yaml(os.getenv('CONFIG_PATH', '../config.yaml'))
    redis_conn = init_redis(cf['REDIS'])

    logging.info('data_server was successfully started')

    while True:
        task = None
        try:
            task = get_save_image_task(redis_conn)
        except Exception as e:
            logging.error(f'Cannot parse task from queue. Exception: {e}')
        if task:
            try:
                save_image(task, cf)
            except Exception as e:
                logging.error(f'Cannot save image. Filetime: {task.time} Exception: {e}')
