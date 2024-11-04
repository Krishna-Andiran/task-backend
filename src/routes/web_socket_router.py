
from fastapi import WebSocket, APIRouter
from src.controller.web_socket_controller import websocket_handler as ws_handler

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"]
)

@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    await ws_handler(websocket)
