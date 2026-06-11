from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

def main():
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    main()