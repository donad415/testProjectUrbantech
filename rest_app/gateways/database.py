from dependency_injector import containers, providers, resources
from sqlalchemy import create_engine


class DatabaseResource(resources.AsyncResource):
    async def init(self, user, password, host, port, db_name):
        return create_engine(
            'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
                user=user,
                password=password,
                host=host,
                port=port,
                db_name=db_name
            )
        )

    async def shutdown(self, resource: init) -> None:
        await resource.close()
