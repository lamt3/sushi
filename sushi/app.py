from fastapi import FastAPI, APIRouter
# from sushi.tuna.dao.company_dao import CompanyDAO
# from sushi.tuna.dbs.postgres import PostgresDB
from tuna.handlers.home_handler import HomeHandler
# from sushi.tuna.services.home_service import HomeService



def initialize():
    app = FastAPI()

    # pg_db = PostgresDB()
    # company_dao = CompanyDAO(db=pg_db)
    # home_service = HomeService(company_dao)

    @app.on_event("shutdown")
    def shutdown():
        # cleanup
        print('shutting down')
        # pg_db.dispose()
    home_handler = HomeHandler()
    app.include_router(home_handler.router)
    return app

app = initialize()


    
    

