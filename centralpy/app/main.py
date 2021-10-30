import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def home():
    data = {
        "text": "hi"
    }
    return {"data": data}


@app.get("/page/{page_name}")
async def page(page_name: str):
    data = {
        "page": page_name
    }
    return {"data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
