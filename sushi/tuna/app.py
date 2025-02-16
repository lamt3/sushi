from fastapi import FastAPI, APIRouter
# from tuna.handlers.connection_handler import ConnectionHandler
from tuna.dbs.base import BaseDB
from tuna.dao.company_dao import CompanyDAO
from tuna.dbs.postgres import PostgresDB
from tuna.handlers.home_handler import HomeHandler
from tuna.services.home_service import HomeService
from tuna.config import setup_logging
import logging

logger = logging.getLogger(__name__)

def initialize():
    # Setup logging first
    setup_logging()
    
    app = FastAPI()
    logger.info("Initializing application...") 

    pg_db = PostgresDB()
    session = pg_db.create_db()
  
    company_dao = CompanyDAO(db=session)
    home_service = HomeService(company_dao)
    home_handler = HomeHandler(home_service)

    # connection_handler = ConnectionHandler()

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Shutting down application...")
        await pg_db.dispose()

    @app.on_event("startup")
    async def startup():
        try:
            logger.info("Testing database connection...")
            await pg_db.test_connection()
            logger.info("Database connection successful")
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


    
    

