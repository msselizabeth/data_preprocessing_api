from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def heath_check():
    return {"status": "ok", "message": "Hello from Data Proccessing API !"}