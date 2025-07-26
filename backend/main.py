from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.admin import admin_router
from routes.auth import auth_router
from routes.users import user_router
from models import Base
from database import engine
from logger import configure_logging, LogLevels
import logging
from config import min_log_level

app = FastAPI(root_path="/api")
Base.metadata.create_all(bind=engine)



origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)


def main():
    pass
    
    

if __name__ == '__main__':
    configure_logging(log_level=min_log_level)
    logging.info("Application invoked")
    logging.info("Starting FastAPI server")
    # start uvicorn server to host the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    main()