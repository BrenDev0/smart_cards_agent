import logging
from src.core.dependencies.container import Container
from src.core.domain.exceptions.dependencies import DependencyNotRegistered

from src.features.files.services.sheets_service import SheetsService

logger = logging.getLogger(__name__)

def get_sheets_service() -> SheetsService:
    try:
        instance_key = "sheets_service"
        service = Container.resolve(instance_key)
    except DependencyNotRegistered:
        service = SheetsService()
        Container.register(instance_key, service)
        logger.info(f"{instance_key} registerd")
    
    return service