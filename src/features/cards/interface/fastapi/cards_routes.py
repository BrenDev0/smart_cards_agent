from uuid import UUID
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
import json
from src.app.interface.fastapi.schemas.responses import RequestReceived
from src.llm.dependencies.use_cases import get_rows_to_cards_use_case
from src.features.cards.services.sheets_service import SheetsService
from src.features.cards.dependencies.services import get_sheets_service
from src.llm.application.use_cases.rows_to_cards import RowsToCards
from  src.app.middleware.hmac import verify_hmac

router = APIRouter(
    prefix="/api/cards",
    tags=["cards"],
)

@router.post("/extract-from-file/{connection_id}", status_code=202, response_model=RequestReceived)
async def process_file(
    backgroundTasks: BackgroundTasks,
    connection_id: UUID,
    file: UploadFile = File(...),
    _: None = Depends(verify_hmac),
    sheets_service: SheetsService = Depends(get_sheets_service),
    rows_to_cards: RowsToCards = Depends(get_rows_to_cards_use_case)
):
    """
        # HMAC protected 

        ## allowed file types: 
        - csv
        - xlsx
        - xls
    """
    try:
        if not file.filename.endswith((".csv", ".xlsx", ".xls")):
            raise HTTPException(400, "File must be csv, xlsx, or xls")
        
        filename = file.filename
        content = await file.read()

        rows = sheets_service.parse_file_to_dicts(filename=filename, content=content)


        backgroundTasks.add_task(
            rows_to_cards.execute,
            connection_id,
            rows
        )

        return RequestReceived()

    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unable to process request at this time.") 
    

    