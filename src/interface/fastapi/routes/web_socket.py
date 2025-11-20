from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect
from uuid import UUID
from src.features.websocket.middleware.hmac import verify_hmac_ws
from src.features.websocket.connections import WebsocketConnectionsContainer


router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket("/{connection_id}")
async def websocket_interact(websocket: WebSocket, connection_id: UUID):
    await websocket.accept()
    params = websocket.query_params
    signature = params.get("x-signature")
    payload = params.get("x-payload")

    if not await verify_hmac_ws(signature, payload):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    WebsocketConnectionsContainer.register_connection(connection_id, websocket)
    
    print(f'Websocket connection: {connection_id} opened.')
    try:
        while True: 
            await websocket.receive_text()

    except WebSocketDisconnect:
        WebsocketConnectionsContainer.remove_connection(connection_id)
        print(f'Websocket connection: {connection_id} closed.')