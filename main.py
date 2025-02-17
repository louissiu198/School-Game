from typing import Annotated
from pydantic import BaseModel
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
    Request,
    Response,
    Form
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from json import loads, load, dump
from users import Users
from datetime import datetime, timedelta, timezone
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

user_cli: Users = Users()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change this to specify allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Login(BaseModel):
#     username: str
#     password: str


# class Register(BaseModel):
#     username: str
#     password: str

async def check_status(authorization: object) -> bool:
    if authorization:
        if user_cli.check_db_item("token", authorization): # elif not required
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER) 

async def response_json(status: str = "success", response: str = "", data: dict = {}) -> dict:
    return {
        "status": status,
        "response": response,
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
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER) 
    return templates.TemplateResponse(
        request=request, name="users.html", context={"webTitle": "Register", "buttonRedirect": "Login", "linkAction": "register"}
    )

@app.get("/login", response_class = HTMLResponse)
async def login_page(request: Request, authorization: str = Cookie(None)) -> HTMLResponse:
    if authorization:
        if user_cli.check_db_item("token", authorization): # elif not required
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER) 
    return templates.TemplateResponse(
        request=request, name="users.html", context={"webTitle": "Login", "buttonRedirect": "Register", "linkAction": "login"}
    )

@app.post("/api/register")
async def register(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    if user_cli.check_db_item("username", username):
        return await response_json("error", "Username Is Already Registered!")
    # elif user_cli.check_db_item("password", password):
    #     return await response_json("error", "Password Is In The Database!")
    elif request.cookies.get("authorization") != None:
        return await response_json("error", "Don't tryna register the second time!")
    token = user_cli.create_user(username, password)
    response.set_cookie("authorization", token, expires = datetime.now(timezone.utc) + timedelta(days=7))
    return {
        "status": "success",
        "message": "account created"
    }

@app.post("/api/login")
async def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user_info: dict = user_cli.fetch_account_info(username) # none or dict
    print(user_info)
    if type(user_info) is dict:
        if password == user_info["password"]:
            response.set_cookie("authorization", user_info["token"], expires = datetime.now(timezone.utc) + timedelta(days=7))
            return await response_json("success", "Login Successfully!", {"token": user_info["token"]})
        else:
            return await response_json("error", "Please check if password is correct!")
    return await response_json("error", "Please check if email is correct!")




async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect as e:
        print(f"Client disconnected: {e}")


@app.get("/join/{game_id}")
async def join_game(game_id: int, q: str = None):
    return {"item_id": game_id, "query": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3333)



    # data = {
    #     "map_name": "showdown",

    # }