from pydantic import BaseModel
from typing import Optional, List
from src.core.domain.entities.message import Message

class WorkflowState(BaseModel):
    llm_response: Optional[str] = None
    chat_history: Optional[List[Message]] = None

class ClientInfo(BaseModel):
    messaging_product: str
    contact_identifier: str

class SessionState(BaseModel):
    session_id: str
    workflow: WorkflowState
    client: ClientInfo