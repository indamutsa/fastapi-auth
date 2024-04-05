# a simpple fastapi app
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

app = FastAPI()

# Endpoints
@app.get("/test")
async def test():
    return {"message": "Hello World"}
