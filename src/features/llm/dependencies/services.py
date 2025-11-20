import logging

from src.core.dependencies.container import Container
from src.core.domain.exceptions.dependencies import DependencyNotRegistered

from src.features.llm.application.services.prompt_service import PromptService

from src.features.llm.domain.services.llm_service import LlmService
from src.features.llm.infrastructure.langchain.llm_service import LangchainLlmService



logger = logging.getLogger(__name__)

def get_llm_service() -> LlmService:
    try:
        instance_key = "llm_service"
        service = Container.resolve(instance_key)
    except DependencyNotRegistered:
        service = LangchainLlmService()
        Container.register(instance_key, service)
        logger.info(f"{instance_key} registered")
    
    return service

def get_prompt_service() -> PromptService:
    try:
        instance_key = "prompt_service"
        service = Container.resolve(instance_key)
        

    except DependencyNotRegistered:
        service = PromptService()
        Container.register(instance_key, service)
        logger.info(f"{instance_key} registered")

    return service

