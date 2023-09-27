from sqlalchemy import create_engine

from app import app
import os

from rest_app.containers import Container

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    app.run("0.0.0.0", port=os.getenv('PORT', 6969))
