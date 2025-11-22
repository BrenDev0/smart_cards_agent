from typing import Any, Dict, List, Union
from uuid import UUID
import logging
import asyncio

from src.llm.application.agents.card_parser import CardParser
from src.shared.services.ws_transport import WebSocketTransportService
from src.llm.domain.exceptions.llm_service import LlmInvokeError
logger = logging.getLogger(__name__)

class RowsToCards:
    def __init__(
        self,
        smart_card_parser: CardParser,
        ws_transport: WebSocketTransportService
    ):
        self.__smart_card_parser = smart_card_parser
        self.__ws_tranport = ws_transport 
        self.__max_retries  = 3
    
    async def execute(
        self,
        ws_connection_id: Union[str, UUID],
        rows_dicts: List[Dict[str, Any]]
    ):
        cards = []
        for row in rows_dicts:
            retries = 0
            while retries < self.__max_retries:
                try:
                    card = await self.__smart_card_parser.interact(
                        input=row
                    )

                    cards.append(card)

                    await self.__ws_tranport.send(
                        connection_id=ws_connection_id,
                        data=card
                    )

                    break
                except LlmInvokeError as e:
                    logger.error(f"LLM error on attempt {retries + 1}: {e}")
                    retries += 1
                    if retries < self.__max_retries:
                        await asyncio.sleep(1)
            
                except Exception as e:
                    logger.error(
                        f"Error parsing {row}::::{str(e)}"
                    )

                    break
            
            if retries >= self.__max_retries:
                logger.error(f"Max retries exceeded for row: {row}")
        
        return cards


                

            