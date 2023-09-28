import logging
import os
import sys
import time

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

    logging.info("image_handler was successfully started")

    while True:
        task = get_handle_image_task(redis_conn)
        if task:
            handle_image(task, cf, redis_conn)
        time.sleep(1)
