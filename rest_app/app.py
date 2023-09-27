import os

from flasgger import Swagger
from flask import Flask, request, abort
from flask_pydantic import validate
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename

from rest_app.dto.api_request.image import UploadImageRequest
from rest_app.utils.yaml_reader import read_yaml

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/api/images', methods=["POST"])
@validate()
def index(form: UploadImageRequest):
    """ Загрузка нового изображения
    ---
    parameters:
      - name: description
        in: formData
        type: string
        required: true
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Изображение успешно загружено
    """
    if not (file := request.files.get('file')):
        abort(400)
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['FILE_EXT']:
            return 'Неверное расширение', 400
        file.save(os.path.join(app.config['UPLOAD_FILE_DIR'], filename))

    return f"Hello {form.description}!!"


if __name__ == "__main__":
    cf = read_yaml("../config.yaml")
    app.config.update(cf)

    db_master_config = app.config['DB_MASTER']
    db = create_engine(
        'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=db_master_config['USER'],
            password=db_master_config['PASS'],
            host=db_master_config['HOST'],
            port=db_master_config['PORT'],
            db_name=db_master_config['DB_NAME']
        )
    )

    app.run("0.0.0.0", port=os.getenv('PORT', 6969))
