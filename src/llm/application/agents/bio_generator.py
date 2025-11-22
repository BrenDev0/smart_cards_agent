from typing import Any, Dict
import logging
from src.llm.domain.services.llm_service import LlmService
from src.llm.application.services.prompt_service import PromptService
logger = logging.getLogger(__name__)

class BioGenerator:
    def __init__(
        self, 
        llm_service: LlmService, 
        prompt_service: PromptService,
    ):
        self.__llm_service = llm_service
        self.__prompt_service = prompt_service
    
    def __get_prompt(
        self,
        input: Dict[str, Any]
    ):
        system_message = f"""
        You are an expert at writing short bios for clients

        given the data recieved form  the client Write a short bio 30 words or less for thier profile

        IMPORTANT
        - Your answer will always be in spanish
        - you answer willnever  be longer than 30 words
        """

        prompt = self.__prompt_service.build_prompt(
            system_message=system_message,
            input=input
        )

        return prompt
    

    async def interact(
        self,
        input: Dict[str, Any]
    ):
           
        prompt = self.__get_prompt(
            input=input
        )

        response = await self.__llm_service.invoke(
            prompt=prompt,
            temperature=1.3
        )
    
        return response
        



        

        