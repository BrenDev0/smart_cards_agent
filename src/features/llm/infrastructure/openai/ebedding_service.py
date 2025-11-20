import tiktoken
import os
from typing import List
from openai import AsyncOpenAI

from src.features.llm.domain.services.embedding_service import EmbeddingService

class OpenAIEmbeddingService(EmbeddingService):
    def __init__(self, model: str = "text-embedding-3-large"):
        self.__api_key = os.getenv("OPENAI_API_KEY")

        if not self.__api_key:
            raise ValueError("Openai variables not configured")
        
        self._client = AsyncOpenAI(api_key=self.__api_key)
        self._model = model
        self._encoding = tiktoken.get_encoding("cl100k_base")
    
    async def embed_query(self, query: str) -> List[float]:
        """Embed a single query"""
        result = await self._client.embeddings.create(
            model=self._model,
            input=query
        )
        return result.data[0].embedding