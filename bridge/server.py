# bridge/server.py
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .comm_handler import CommHandler
from utils.config import BRIDGE_HOST, BRIDGE_PORT, WS_PING_INTERVAL

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

comm = CommHandler()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # handle incoming messages non-blocking
            try:
                data = await asyncio.wait_for(ws.receive_text(), timeout=WS_PING_INTERVAL)
                payload = json.loads(data)
                # expected payloads:
                # { "type": "command", "data": "forward" }
                # { "type": "mode", "data": "auto" }
                if payload.get("type") == "command":
                    cmd = payload.get("data")
                    comm.publish_command(cmd)
                elif payload.get("type") == "mode":
                    mode = payload.get("data")
                    comm.publish_mode(mode)
            except asyncio.TimeoutError:
                # no incoming message, proceed to send telemetry
                pass
            except WebSocketDisconnect:
                break
            except Exception as e:
                # ignore bad messages and continue
                print("[bridge] recv error:", e)

            # Send latest telemetry back
            telemetry = comm.get_latest_data()
            message = {"type": "telemetry", "data": telemetry}
            try:
                await ws.send_text(json.dumps(message, default=str))
            except Exception:
                # connection might be closed; break out
                break

    finally:
        try:
            await ws.close()
        except:
            pass

if __name__ == "__main__":
    uvicorn.run("bridge.server:app", host=BRIDGE_HOST, port=BRIDGE_PORT, log_level="info")
