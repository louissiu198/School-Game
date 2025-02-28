from typing import Annotated
from pydantic import BaseModel
from helper import Game
from fastapi import (
    Cookie,
    FastAPI,
    WebSocket,
    WebSocketException,
    status,
    Request,
    Response,
)
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run
from json import loads, dumps
from users import Users
from datetime import datetime, timedelta, timezone
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

user_cli: Users = Users()
game_temp: dict = {}
templates = Jinja2Templates(directory="pages")


class UsersModel(BaseModel): # inter usage between register/login
    username: str
    password: str

    
class LobbyModel(BaseModel):
    gamename: str

app.add_middleware( # i didn't know why i added this
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def check_status(authorization: object) -> bool:
    if authorization:
        if user_cli.check_db_item("token", authorization): # elif not required
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER) 

async def response_json(status: str = "success", response: str = "", data: dict = {}) -> dict:
    return {
        "status": status,
        "message": response,
        "data": data
    }

@app.get("/", response_class = HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/game", response_class = HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="game.html"
    )

@app.get("/register", response_class = HTMLResponse)
async def register_page(request: Request, authorization: str = Cookie(None)) -> HTMLResponse:
    if authorization:
        if user_cli.check_db_item("token", authorization): # elif not required
            return RedirectResponse("/lobby", status_code=status.HTTP_303_SEE_OTHER) 
    return templates.TemplateResponse(
        request=request, 
        name="users.html", 
        context={
            "webTitle": "Register", 
            "buttonRedirect": "Login", 
            "linkAction": "register", 
            "linkRedirect": "login"
        }
    )

@app.get("/login", response_class = HTMLResponse)
async def login_page(request: Request, authorization: str = Cookie(None)) -> HTMLResponse:
    if authorization:
        if user_cli.check_db_item("token", authorization):
            return RedirectResponse("/lobby", status_code=status.HTTP_303_SEE_OTHER) 
    return templates.TemplateResponse(
        request=request, 
        name="users.html",
        context={
            "webTitle": "Login", 
            "buttonRedirect": "Register", 
            "linkAction": "login", 
            "linkRedirect": "register"
        }
    )

@app.get("/lobby", response_class = HTMLResponse)
async def lobby_page(request: Request, authorization: str = Cookie(None)) -> HTMLResponse:
    if authorization:
        if user_cli.check_db_item("token", authorization): 
            return templates.TemplateResponse(
                request=request, name="lobby.html"
            )
    return RedirectResponse("/register", status_code=status.HTTP_303_SEE_OTHER) 

@app.get("/lobby/{session_id}", response_class = HTMLResponse)
async def join_game(session_id: str, request: Request, authorization: str = Cookie(None)) -> HTMLResponse:
    if authorization:
        if session_id in game_temp:
            if user_cli.check_db_item("token", authorization): 
                return templates.TemplateResponse(
                    request=request, name="game.html", context = {
                        "game_session": session_id
                    }
                )
        else:
            return RedirectResponse("/lobby", status_code=status.HTTP_307_TEMPORARY_REDIRECT) 
    return RedirectResponse("/register", status_code=status.HTTP_303_SEE_OTHER) 
    

@app.post("/api/register")
async def register(request: Request, response: Response, user_data: UsersModel):
    if user_cli.check_db_item("username", user_data.username):
        return await response_json("error", "Username Is Already Registered!")
    # elif user_cli.check_db_item("password", password):
    #     return await response_json("error", "Password Is In The Database!")
    elif request.cookies.get("authorization") != None:
        return await response_json("error", "Don't tryna register the second time!")
    token = user_cli.create_user(user_data.username, user_data.password)
    response.set_cookie("authorization", token, expires = datetime.now(timezone.utc) + timedelta(days=7))
    return await response_json("success", "account created")

@app.post("/api/login")
async def login(response: Response, user_data: UsersModel):
    user_info: dict = user_cli.fetch_account_info(user_data.username) # none or dict
    if type(user_info) is dict:
        if user_data.password == user_info["password"]:
            response.set_cookie("authorization", user_info["token"], expires = datetime.now(timezone.utc) + timedelta(days=7))
            return await response_json("success", "Login Successfully!", {"token": user_info["token"]})
        else:
            return await response_json("error", "Please check if password is correct!")
    return await response_json("error", "Please check if username is correct!")

@app.post("/api/create")
async def create_game(lobby_data: LobbyModel, authorization: str = Cookie(None)):
    global game_temp
    if authorization:
        while True: # should let a function to do the whole thing - no time
            game_id = str(uuid4()).replace("-", "")
            if game_id not in game_temp:
                break
        game_temp[game_id] = Game(lobby_data.gamename)
        return await response_json("success", game_id)
    return await response_json("redirect", "Please ensure you are logged in")

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            json_data = loads(data) # parse json string
            print(json_data)
            await websocket.send_text(dumps({
                "message": "success"
            }))
    except WebSocketDisconnect as e:
        print(f"Client disconnected: {e}")



if __name__ == "__main__":
    run(app, host="0.0.0.0", port=3333)

"""
6 underwear
1 plain socks
1 pe socks
2 blue socks (1 pe inside)
4 bottle of water

2 school trousers
"""