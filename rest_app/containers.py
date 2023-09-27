from dependency_injector import containers, providers

from rest_app.gateways import Gateways


class Container(containers.DeclarativeContainer):
    _cfg = providers.Configuration()
    #_cfg.from_pydantic(AppSettings)

    gateways = providers.Container(
        Gateways,
        #cfg=_cfg,
    )

    # repositories = providers.Container(
    #     Repositories,
    #     cfg=_cfg,
    #     gateways=gateways,
    # )
    #
    # services = providers.Container(
    #     Services,
    #     cfg=_cfg,
    #     gateways=gateways,
    #     repositories=repositories,
    # )
    #
    # controllers = providers.Container(
    #     Controllers,
    #     cfg=_cfg,
    #     services=services,
    # )
    #
    # middlewares = providers.Container(
    #     Middlewares,
    #     cfg=_cfg,
    #     services=services,
    # )
    #
    # routers = providers.Container(
    #     Routers,
    #     cfg=_cfg,
    #     controllers=controllers,
    #     middlewares=middlewares,
    # )
    #
    # application = providers.Singleton(
    #     Application,
    #     title=_cfg.swagger_title,
    #     description=_cfg.swagger_description,
    #     version=_cfg.swagger_version,
    #     routers=routers,
    #     middlewares=middlewares,
    #     libraries=libraries,
    # )