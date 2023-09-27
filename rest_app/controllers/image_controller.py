from app import app
from dependency_injector.wiring import Provide, inject
from sqlalchemy import Engine

from rest_app.containers import Container


@app.route("/")
@app.route("/<name>")
@inject
def index(name='Anonymous', db: Engine = Provide[Container.gateways.db_client]):

    return f"Hello {name}!!"
