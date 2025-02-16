from fastapi import APIRouter

from tuna.services.home_service import HomeService

class HomeHandler:
    def __init__(self, hs: HomeService):
        self.hs = hs

    async def health(self):
        return await self.hs.get_home()
