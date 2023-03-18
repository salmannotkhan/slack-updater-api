from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi import Depends, FastAPI
from .plugins.client import SlackClient
from os import environ
from pydantic import BaseModel

client_id = environ.get("CLIENT_ID")
client_secret = environ.get("CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("Missing environment variables: CLIENT_ID, CLIENT_SECRET")

slack = SlackClient(client_id, client_secret)

class Code(BaseModel):
    code: str

class Status(BaseModel):
    status_text: str
    status_emoji: str
    status_expiration: int


app = FastAPI(
    title="Slack Updater API",
    contact={
        "name": "Salman Shaikh",
        "url": "https://salmannotkhan.github.io/",
        "email": "tony903212@gmail.com",
    },
)

bearer = HTTPBearer(auto_error=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {
        "Welcome to": "Slack Updater API",
        "For docs": "Visit /docs",
        "For redocs": "Visit /redoc",
    }

@app.post("/token")
async def get_token(code: Code):
    return slack.get_access_token(code.code)

@app.get("/emojis")
async def get_emojis(token=Depends(bearer)):
    return slack.get_emojis(token.credentials)

@app.post("/status")
async def set_status(status: Status, token=Depends(bearer)):
    return slack.set_status(token.credentials, status.dict())
