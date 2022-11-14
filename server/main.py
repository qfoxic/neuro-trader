from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/match")
async def root():
    return {"message": "Hello World"}
