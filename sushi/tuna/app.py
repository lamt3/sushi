from fastapi import FastAPI, APIRouter
from tuna.dbs.base import BaseDB
from tuna.dao.company_dao import CompanyDAO
from tuna.dbs.postgres import PostgresDB
from tuna.handlers.home_handler import HomeHandler
from tuna.services.home_service import HomeService



def initialize():
    app = FastAPI()

    # pg_db = PostgresDB()
    # company_dao = CompanyDAO(db=pg_db)
    # home_service = HomeService(company_dao)
    home_handler = HomeHandler()

    @app.on_event("shutdown")
    def shutdown():
        # cleanup
        print('shutting down')
        # pg_db.dispose()

   
    routes = APIRouter(prefix="/api/v1")
    routes.add_api_route("/health", home_handler.health, methods=["GET"])
    app.include_router(routes)
    return app

app = initialize()


    
    

