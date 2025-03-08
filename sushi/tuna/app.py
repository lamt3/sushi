from openai import OpenAI
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tuna.dtos.shopify_dao import ShopifyDAO
from tuna.handlers.pixel_handler import PixelHandler
from tuna.handlers.ad_handler import AdHandler
from tuna.services.ad_service import AdService
from tuna.dao.ad_dao import AdDAO
from tuna.auth.auth_middleware import auth_middleware
from tuna.dbs.base import get_db
from tuna.handlers.connection_handler import ConnectionHandler
from tuna.dao.member_dao import MemberDAO
from tuna.handlers.home_handler import HomeHandler
from tuna.services.home_service import HomeService
from tuna.config import Config, setup_logging
import logging


logger = logging.getLogger(__name__)

def initialize():

    setup_logging()

    app = FastAPI()
    
    logger.info("Initializing application...") 

    origins = [
        "*",
        "https://*.myshopify.com",       # All Shopify stores
        "https://*.shopifypreview.com",  # Preview/development stores
        "https://*.shopify.com",         # Shopify admin
        "https://shopify.dev", 
        "http://localhost:3000", 
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

    ai_client = OpenAI(api_key=Config.OPEN_AI_KEY)
    
    pg_db = get_db("postgres")
    session = pg_db.create_db()
  
    # set up daos
    company_dao = MemberDAO(db=session)
    shopify_dao = ShopifyDAO(session)
    ad_dao = AdDAO(db=session)

    # set up services
    home_service = HomeService(company_dao, shopify_dao)
    ad_service = AdService(ad_dao)
    
    # set up handlers
    home_handler = HomeHandler(home_service)
    connection_handler = ConnectionHandler(ad_service, home_service)
    ad_handler = AdHandler(ad_service)
    pixel_handler = PixelHandler()

    #set up routes
    routes = APIRouter(prefix="/api/v1")
    routes.add_api_route("/health", home_handler.health, methods=["GET"])
    routes.add_api_route("/login", home_handler.login_member, methods=["POST"])
    routes.add_api_route("/auth/status", home_handler.verify_auth, methods=["GET"])
    
    routes.add_api_route("/dashboard", home_handler.get_dashboard, methods=["GET"])

    #Connection Routes
    routes.add_api_route("/shopify/oauth", connection_handler.initiate_shopify_oauth, methods=["GET"])
    routes.add_api_route("/shopify/oauth/callback", connection_handler.shopify_oauth, methods=["GET"])

    routes.add_api_route("/destination/oauth/{ad_platform}", connection_handler.get_auth_url, methods=["GET"])
    routes.add_api_route("/destination/oauth/{ad_platform}/callback", connection_handler.get_oauth_token, methods=["GET"])

    routes.add_api_route("/ad/{ad_platform}/accounts", ad_handler.get_ad_accounts, methods=["GET"])
    routes.add_api_route("/ad/{ad_platform}/accounts", ad_handler.add_ad_accounts, methods=["POST"])

    routes.add_api_route("/pixel", pixel_handler.process_event, methods=["POST"])

    app.include_router(routes)

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


    return app

app = initialize()


    
    

