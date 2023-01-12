from fastapi import APIRouter
from application.service import websocket_service
from fastapi.websockets import WebSocket

router = APIRouter()


@router.websocket('/{message_name}', name='websockets数据')
def web_socket(message_name, websocket: WebSocket):
    return websocket_service.websocket_data(name=message_name, websocket=websocket)
