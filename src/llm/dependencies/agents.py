import logging

from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.llm.application.agents.card_parser import CardParser
from src.llm.application.agents.bio_generator import BioGenerator
from src.llm.dependencies.services import get_llm_service, get_prompt_service
logger = logging.getLogger(__name__)


def get_card_parser_agent() -> CardParser:
    try:
        instance_key = "card_parser_agent"
        agent = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        agent = CardParser(
            llm_service=get_llm_service(),
            prompt_service=get_prompt_service()
        )

        Container.register(instance_key, agent)
        logger.info(f"{instance_key} registered")

    return agent


def get_bio_generator_agent() -> BioGenerator:
    try:
        instance_key = "bio_generator_agent"
        agent = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        agent = BioGenerator(
            llm_service=get_llm_service(),
            prompt_service=get_prompt_service()
        )

        Container.register(instance_key, agent)
        logger.info(f"{instance_key} registered")

    return agent