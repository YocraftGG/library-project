from fastapi import FastAPI
import uvicorn

from logs.setup_logger import logger
from database import db_connection
from routes import book_routes
from routes import member_routes
from routes import report_routes

app = FastAPI()
app.include_router(book_routes.router, prefix="/books")
app.include_router(member_routes.router, prefix="/members")
app.include_router(report_routes.router, prefix="/reports")

def main():
    db_connection.create_tables()
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    main()