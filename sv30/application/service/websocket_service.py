import asyncio
from fastapi.websockets import WebSocket
from infrastructure.utils.websocket_helper import ConnectionManager
from infrastructure.dao.redis_setting import redis_conn


async def websocket_data(name, websocket: WebSocket):
    manager = ConnectionManager()
    data = {}
    redis_data = None
    await manager.connect(websocket)
    try:
        while True:
            if redis_conn.llen(name) > 0:
                redis_data = redis_conn.blpop(name)
                data['data'] = str(redis_data[1])
                print(data['data'])
                data['comment'] = name
                await manager.send_message(message=data, websocket=websocket)
            await asyncio.sleep(1)
    except:
        manager.disconnect(websocket)
        redis_conn.rpush(name, str(redis_data[1]))
        await websocket.close()
