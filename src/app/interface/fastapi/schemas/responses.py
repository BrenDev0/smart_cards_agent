from pydantic import BaseModel

class RequestReceived(BaseModel):
    detail: str = "Request received"