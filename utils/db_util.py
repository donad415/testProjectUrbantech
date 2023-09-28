import os

from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.yaml_reader import read_yaml

db_config = read_yaml(os.getenv('CONFIG_PATH', '../config.yaml'))['DB_MASTER']
engine = create_engine(
    'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
        user=db_config['USER'],
        password=db_config['PASS'],
        host=db_config['HOST'],
        port=db_config['PORT'],
        db_name=db_config['DB_NAME'],
    )
)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class ImageEntity(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    filepath = Column(String(255))
    time = Column(DateTime)
