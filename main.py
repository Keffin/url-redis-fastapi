from fastapi import FastAPI, Response, status
from storage.service import Service
from pydantic import BaseModel
from shortener.shortener import createShortLink
import uvicorn

app: FastAPI = FastAPI()
service = Service()


class UrlRequest(BaseModel):
    long_url: str


class UrlResponse(BaseModel):
    message: str
    short_url: str
    status_code: int


class Handler:
    def __init__(self):
        pass

    def create_short_url(self, url_request: UrlRequest) -> dict:
        short_url: str = createShortLink(url_request.long_url)
        service.setUrlMapping(short_url, url_request.long_url)
        res: str = "localhost:8000/" + short_url
        return {
            "message": "successfully shortened",
            "url": res,
            "status": 201
        }


handler = Handler()


@app.get("/")
async def read_root():
    res = service.ping()
    return {"message": res}


@app.post("/create-url")
async def create_url(url_request: UrlRequest, response_model=UrlResponse):
    res = handler.create_short_url(url_request)
    response = UrlResponse(message=res["message"], short_url=res["url"], status_code=res["status"])
    return response


@app.get("/get-url/{url}")
async def get_url(url: str):
    short_url = url
    initial_url = service.getUrlMapping(short_url)
    return {"url": initial_url}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)