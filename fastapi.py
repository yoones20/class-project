from fastapi import FastAPI, WebSocket

app = FastAPI()

# لیستی برای ذخیره کلاینت‌های متصل شده
clients = []

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # ارسال پیام به همه کلاینت‌ها
            for client in clients:
                await client.send_text(f"Client {client_id}: {data}")
    finally:
        # حذف کلاینت از لیست هنگام قطع شدن اتصال
        clients.remove(websocket)