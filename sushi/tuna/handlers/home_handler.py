from fastapi import APIRouter

from tuna.services.home_service import HomeService

class HomeHandler:
    # def __init__(self):
        # self.hs = hs

    def health(self):
        return {"Health": "OK!"}
