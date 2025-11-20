from src.core.dependencies.container import Container
from src.core.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.services.ws_transport import WebSocketTransportService


def get_ws_transport() ->WebSocketTransportService:
    try: 
        instance_key = "ws_transport"
        service = Container.resolve(instance_key)
    except DependencyNotRegistered:
        service = WebSocketTransportService()

        Container.register(instance_key, service)

    return service