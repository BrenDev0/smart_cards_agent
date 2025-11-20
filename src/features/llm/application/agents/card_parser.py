from typing import Any, Dict, List
import logging
from src.core.domain.entities.smart_card import SmartCard
from src.features.llm.domain.services.llm_service import LlmService
from src.features.llm.application.services.prompt_service import PromptService
from src.features.llm.domain.exceptions.llm_service import LlmInvokeError
logger = logging.getLogger(__name__)

class CardParser:
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
        You are a data mapping specialist. Your task is to convert CSV row data into a structured SmartCard object.

        ## Instructions:
        1. **Analyze the provided CSV key-value pairs**
        2. **Map CSV keys to SmartCard fields** by looking for similar names, abbreviations, or variations
        3. **Clean and format the data** appropriately for each field
        4. **Return a valid SmartCard JSON object**

        ## CSV Data to Process:
        {input}

        ## Mapping Guidelines:
        - Look for field variations mentioned in the schema descriptions
        - Clean URLs (ensure proper format with https://)
        - Normalize social media handles (remove @ symbols for storage)
        - Handle missing required fields gracefully with reasonable defaults
        - Convert phone numbers to consistent format
        - If a CSV key doesn't match any schema field, ignore it
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

        response = await self.__llm_service.invoke_structured(
            prompt=prompt,
            response_model=SmartCard,
            temperature=0.0
        )
    
        return response
        



        

        