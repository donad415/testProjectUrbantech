from dependency_injector import containers, providers

from rest_app.gateways.database import DatabaseResource


class Gateways(containers.DeclarativeContainer):
    #cfg: AppSettings = providers.Configuration()

    db_client = providers.Resource(
        DatabaseResource,
        user='test',
        password='qwerty1234',
        host='localhost',
        port=5435,
        db_name='testdb'
    )
