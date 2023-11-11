from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from mysql import models, schema, connect, user_crud, danger_crud, msg_crud

conn = connect.engineconn()

connect.Base.metadata.create_all(bind=conn.engine)

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_token(token: str = Depends(oauth2_scheme)):
    return token

def create_token(username: str):
    return "access_token_{}".format(username)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

#users
@app.get("/users")
def get_users(db: Session = Depends(conn.getDB)):
    db_users = user_crud.get_users(db)
    return db_users

@app.post("/users", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(conn.getDB)):
    db_user = user_crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    return user_crud.create_user(db=db, user=user)

#dangers
@app.post("/danger", response_model= schema.DangerBase)
def alert_danger(danger: schema.DangerCreate, db: Session = Depends(conn.getDB)):
    return danger_crud.create_danger(db=db, danger=danger)

#login
@app.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(conn.getDB)):
    db_user = user_crud.get_user_by_name(db, name=user.name)
    if db_user:
        if db_user.password == user.password:
            token = create_token(user.name)
            return {"result": "success", "access_token": token}
        else:
            return {"result": "fail"}
    else:
        return {"result": "fail"}

@app.get("/login/test")
def read_protected_data(current_token: str = Depends(get_current_token), db: Session = Depends(conn.getDB)):
    try:
        name = current_token.split("_")[2]
        print(name)
        if user_crud.get_user_by_name(db, name=name):
            return {"message": "This is protected data", "token": current_token}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

#message
@app.get("/message/{template_id}")
def set_message(template_id: str, db: Session = Depends(conn.getDB)):
    message_content = msg_crud.set_message_template(db=db, template_id=int(template_id))
    if message_content is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message_content

@app.post("/reply")
def reply_message(reply: schema.Reply, current_token: str = Depends(get_current_token), db: Session = Depends(conn.getDB)):
    try:
        name = current_token.split("_")[2]
        db_user = user_crud.get_user_by_name(db, name=name)
        if db_user:
            db_user.reply = True
            db.commit()
            db.refresh(db_user)
            return {"result": "success"}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/alert")
def alert_no_reply(db: Session = Depends(conn.getDB)):
    db_users = user_crud.get_users(db)
    no_reply_users = []
    for user in db_users:
        print(user)
        if user.reply == False:
            no_reply_users.append(user)
        user.reply = False

    template = msg_crud.get_active_message_template(db)
    if template is None:
        return {"result": "no sending message"}
    template.activate = False

    db.commit()
    for user in no_reply_users:
        db.refresh(user)

    return no_reply_users

#base test
@app.get("/")
async def root():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_bytes(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("disconnect")
