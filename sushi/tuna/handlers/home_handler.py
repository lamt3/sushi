from fastapi import FastAPI, APIRouter

class HomeHandler:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/hello", self.hello, methods=["GET"])

    def hello(self):
        return {"Hello": "jo"}
