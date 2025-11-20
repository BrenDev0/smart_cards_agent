import logging

from src.core.dependencies.container import Container
from src.core.domain.repositories.session import SessionRepository
from src.core.infrastructure.redis.session_repository import RedisSessionRepository
from src.core.domain.exceptions.dependencies import DependencyNotRegistered

logger = logging.getLogger(__name__)

def get_session_repository() -> SessionRepository:
    try:
        instance_key = "session_repository"
        repository = Container.resolve(instance_key)
        
    except DependencyNotRegistered:
        repository = RedisSessionRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")
        

    return repository