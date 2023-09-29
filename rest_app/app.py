import datetime
import logging
import os
import sys

from flasgger import Swagger
from flask import Flask, request, send_file
from flask_pydantic import validate
from werkzeug.utils import secure_filename

from models.image_task import HandleImageTask
from rest_app.dto.api_request.image import UploadImageRequest, GetImagesRequest
from rest_app.dto.api_response.base.base import BaseResponse
from rest_app.dto.api_response.image import ImageInfo, GetImagesResponse
from utils.db_util import Session, ImageEntity
from utils.redis_util import init_redis, create_handle_image_task
from utils.yaml_reader import read_yaml

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/api/images', methods=["POST"])
@validate()
def upload_image(form: UploadImageRequest):
    """ Загрузка нового изображения
    ---
    parameters:
      - name: description
        in: formData
        type: string
        required: true
        description: Описание изображения
      - name: file
        in: formData
        type: file
        required: true
        description: Файл изображения
    definitions:
      BaseResponse:
        type: object
        properties:
          success:
            type: bool
            required: true
            description: Успешно ли прошёл запрос
          error:
            type: string
            required: false
            description: Описание ошибки
    responses:
      200:
        description: Изображение успешно загружено
        schema:
            $ref: '#/definitions/BaseResponse'
      400:
        description: Ошибка валидации
    """
    if not (file := request.files.get('file')):
        return 'Validation failed. Request must contain file.', 400
    filename = secure_filename(file.filename)
    if filename != '':
        # Проверка соответствия расширения
        # os.path.splitext(filename)[1]
        # if file_ext not in app.config['FILE_EXT']:
        #     return 'Неверное расширение', 400
        task = HandleImageTask(
            filename=filename,
            filedata=file.read(),
            description=form.description,
            time=datetime.datetime.now().timestamp()
        )
        create_handle_image_task(app.config['REDIS_CONN'], task)
        return BaseResponse(success=True)

    return BaseResponse(
        success=False,
        error='Incorrect filename'
    )


@app.route('/api/images', methods=["GET"])
@validate()
def get_images_info(query: GetImagesRequest):
    """ Список информации об обработанных изображениях
        ---
        parameters:
            - in: query
              name: list_start
              required: false
              type: integer
              description: С какого элемента начинается список
            - in: query
              name: list_amount
              required: false
              type: integer
              description: Количество элементов в списке
        definitions:
          GetImagesResponse:
            type: object
            properties:
              item_count:
                type: integer
                description: Всего изображений
              list:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: Идентификатор изображения
                    time:
                      type: string
                      description: Время приёма изображения
                    description:
                      type: string
                      description: Описание изображения
        responses:
          200:
            description: Получаем список
            schema:
                $ref: '#/definitions/GetImagesResponse'
          400:
            description: Ошибка валидации
        """
    with Session() as session:
        images_count = session.query(ImageEntity).count()
        images_info = (session.query(ImageEntity.id, ImageEntity.time, ImageEntity.description)
                       .order_by(ImageEntity.time)
                       .limit(query.limit)
                       .offset(query.offset)
                       .all())

    _list = []
    for image in images_info:
        _list.append(ImageInfo(
            id=image.id,
            description=image.description,
            time=image.time.strftime("%d.%m.%Y, %H:%M:%S")
        ))
    return GetImagesResponse(
        item_count=images_count,
        list=_list
    )


@app.route('/api/images/<path>', methods=["GET"])
@validate()
def download_image(path: int):
    """ Получение обработанного изображения
            ---
            parameters:
                - in: path
                  required: true
                  name: path
                  type: integer
                  description: Идентификатор изображения
            responses:
              200:
                description: Файл изображения
              400:
                description: Ошибка валидации
            """
    with Session() as session:
        image_data = session.get(ImageEntity, path)

    return send_file(image_data.filepath)


def run_application():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )

    cf = read_yaml(os.getenv('CONFIG_PATH', '../config.yaml'))
    app.config.update(cf)

    redis_config = app.config['REDIS']
    conn = init_redis(redis_config)
    app.config['REDIS_CONN'] = conn

    app.run("0.0.0.0", port=app.config['PORT'])
