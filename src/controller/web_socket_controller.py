from fastapi import WebSocket, HTTPException
from starlette import status
from starlette.websockets import WebSocketDisconnect

async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_text()
                if data == "handshake":
                    await websocket.send_text("Handshake successful")
                else:
                    await websocket.send_text(f"Message received: {data}")
            except WebSocketDisconnect:
                print("Client disconnected")
                
                break  # Exit the loop on disconnect
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
                break  # Optionally break the loop on any error
    finally:
        await websocket.close()  # Ensure the socket is closed properly
