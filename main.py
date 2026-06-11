from fastapi import FastAPI, HTTPException
import uvicorn

from database import db_connection

app = FastAPI()

def main():
    db_connection.create_tables()
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    main()