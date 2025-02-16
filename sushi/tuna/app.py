from fastapi import FastAPI, APIRouter
# from tuna.handlers.connection_handler import ConnectionHandler
from tuna.dbs.base import BaseDB
from tuna.dao.company_dao import CompanyDAO
from tuna.dbs.postgres import PostgresDB
from tuna.handlers.home_handler import HomeHandler
from tuna.services.home_service import HomeService
import logging

logger = logging.getLogger(__name__)

def initialize():
    app = FastAPI()

    pg_db = PostgresDB()
    # pg_db.try_connection()
    company_dao = CompanyDAO(db=pg_db)
    home_service = HomeService(company_dao)
    home_handler = HomeHandler(home_service)

    # connection_handler = ConnectionHandler()

    @app.on_event("shutdown")
    async def shutdown():
        # cleanup
        print('shutting down')
        await pg_db.dispose()

    @app.on_event("startup")
    async def startup():
        try:
            print('STARTING DB...')
            print("hostname: " + pg_db.host)
            print("pw: " + pg_db.password)
            print("user: " + pg_db.user)
            print("db: " + pg_db.database)
            await pg_db.test_connection()
            # Store db instance where needed
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    routes = APIRouter(prefix="/api/v1")
    routes.add_api_route("/health", home_handler.health, methods=["GET"])

    #Connection Routes
    # routes.add_api_route("/oauth/{ad_type}", connection_handler.get_auth_url, methods=["GET"])
    # routes.add_api_route("/oauth/{ad_type}/callback", connection_handler.get_oauth_token, methods=["GET"])

    app.include_router(routes)
    return app

app = initialize()


    
    

