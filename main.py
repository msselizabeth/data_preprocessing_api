from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def root():
    return {"status": "ok", "message": "Hello from Data Proccessing API !"}