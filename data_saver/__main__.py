import logging
import os
import time

from data_saver import save_image
from utils.redis_util import init_redis, get_save_image_task
from utils.yaml_reader import read_yaml

if __name__ == '__main__':
    cf = read_yaml(os.getenv('CONFIG_PATH', '../config.yaml'))
    redis_conn = init_redis(cf['REDIS'])

    logging.info("data_server was successfully started")

    while True:
        task = get_save_image_task(redis_conn)
        if task:
            save_image(task, cf)
        time.sleep(1)
