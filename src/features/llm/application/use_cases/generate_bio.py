from typing import Any, Dict

from  src.features.llm.application.agents.bio_generator import BioGenerator


class GernerateBio:
    def __init__(
        self,
        bio_generator: BioGenerator
    ):
        self.__bio_generator = bio_generator

    
    async def execute(
        self,
        user_data: Dict[str, Any]
    ):
        
        bio = await self.__bio_generator.interact(
            input=user_data
        )

        return bio