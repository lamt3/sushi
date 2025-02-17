from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tuna.handlers.connection_handler import ConnectionHandler
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

    connection_handler = ConnectionHandler()

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Shutting down application; disconnecting db...")
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



    origins = [
        "http://localhost:*",  # React dev server
        "https://figsprout.netlify.app*"  # Add production domain
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allow only specified origins
        allow_credentials=True,  # Allow cookies/auth headers
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )
    


    routes = APIRouter(prefix="/api/v1")
    routes.add_api_route("/health", home_handler.health, methods=["GET"])



    #Connection Routes
    routes.add_api_route("/destination/oauth/{ad_platform}", connection_handler.get_auth_url, methods=["GET"])
    routes.add_api_route("/destination/oauth/{ad_platform}/callback", connection_handler.get_oauth_token, methods=["GET"])

    app.include_router(routes)
    return app

app = initialize()


    
    

