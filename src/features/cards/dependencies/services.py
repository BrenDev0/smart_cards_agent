import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.features.cards.services.sheets_service import SheetsService

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