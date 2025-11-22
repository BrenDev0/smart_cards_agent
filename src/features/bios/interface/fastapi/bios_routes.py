from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Depends, Body
from src.app.interface.fastapi.schemas.responses import RequestReceived
from src.app.middleware.hmac import verify_hmac
from src.llm.application.agents.generate_bio import GernerateBio
from src.llm.dependencies.use_cases import get_generate_bio_use_case

router = APIRouter(
    prefix="/api/biographies",
    tags=["biographies"],
)

@router.post("/", status_code=200, response_model=RequestReceived)
async def generate_bio(
    # _: None = Depends(verify_hmac),
    generate_bio: GernerateBio = Depends(get_generate_bio_use_case),
    data: Dict[str, Any] = Body(...)
):
    """
        # HMAC protected 

        ## Accepts a dictionary of any client info
    """
    try:
        bio = await generate_bio.execute(user_data=data)

        return RequestReceived(
            detail=bio
        )

    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unable to process request at this time.") 
    

    