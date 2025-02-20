from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tuna.auth.auth_middleware import auth_middleware
from tuna.dbs.base import get_db
from tuna.handlers.connection_handler import ConnectionHandler
from tuna.dao.member_dao import MemberDAO
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

    origins = [
        "http://localhost:3000",  # React dev server
        "https://figsprout.netlify.app"
    ]

    app.middleware("http")(auth_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allow only specified origins
        allow_credentials=True,  # Allow cookies/auth headers
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
        expose_headers=["*"]
    )

    

    pg_db = get_db("postgres")
    session = pg_db.create_db()
  
    company_dao = MemberDAO(db=session)
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



   

    routes = APIRouter(prefix="/api/v1")
    routes.add_api_route("/health", home_handler.health, methods=["GET"])
    routes.add_api_route("/login", home_handler.login_member, methods=["POST"])
    routes.add_api_route("/auth/status", home_handler.verify_auth, methods=["GET"])
    routes.add_api_route("/dashboard", home_handler.get_dashboard, methods=["GET"])

    #Connection Routes
    routes.add_api_route("/destination/oauth/{ad_platform}", connection_handler.get_auth_url, methods=["GET"])
    routes.add_api_route("/destination/oauth/{ad_platform}/callback", connection_handler.get_oauth_token, methods=["GET"])

    app.include_router(routes)
    return app

app = initialize()


    
    

