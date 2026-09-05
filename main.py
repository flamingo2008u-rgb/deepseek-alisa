from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()
KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    msg = data.get("request", {}).get("command", "")
    async with httpx.AsyncClient() as cl:
        r = await cl.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": msg}]}
        )
    return {"response": {"text": r.json()["choices"][0]["message"]["content"], "end_session": False}}

@app.get("/")
def root():
    return {"ok": True}
