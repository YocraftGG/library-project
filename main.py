from fastapi import FastAPI
import uvicorn

from logs.setup_logger import logger
from database import db_connection
from routes import book_routes

app = FastAPI()
app.include_router(book_routes.router, prefix="/books")

def main():
    db_connection.create_tables()
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    main()