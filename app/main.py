from fastapi import FastAPI, Depends, status, HTTPException, Request, Form, Security
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash
import time
import os

API_KEY = "$2b$12$o7wfxNgH.QFgSSg8lenune9/34VeRRyByi7kqOcWdw.WmATdDUnb6"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'))

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse('homepage.html', {"request": request, "users": users})



# @app.post("/submitform")
# async def form(master: str = Form(...),leverage_value: str = Form(...), secret:str = Form(...), db: Session = Depends(get_db)):
#     values = [master, leverage_value, secret]
#     print(values)
#     # adding_user(values)
#     user_secret = values[2]
#     print()
#     user_master = True
#     user_leverage_value = 1021.07
#     print(type(user_leverage_value))
#     print(type(secret))
#     new_user = models.User(secret=user_secret, master=user_master, leverage_value=user_leverage_value)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     # return {"message": "Hello World"}
    #return templates.TemplateResponse("master.html", {"request": request})


# @app.post('/user', response_model=schemas.ShowUser, tags=['users'])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     user_apikey = Hash.bcrypt(str(time.time()))
#     user_secret = request.secret
#     user_master = request.master
#     user_leverage_value = request.leverage_value
#     new_user = models.User(apikey=user_apikey, secret=user_secret, master=user_master, leverage_value=user_leverage_value)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
#     return user


@app.post('/isMaster')
async def choice(request:Request,db: Session = Depends(get_db)):
    user_choice = await request.json()
    print(user_choice)
    print(user_choice["is_master"])
    print(type(user_choice["is_master"]))
    # {'is_master': 'no', 'leverage_type': 'Fixed leverage', 'l_val': '34', 'selected_master': 'MASTER 3'}
    if user_choice["is_master"] == 'no':
        if  user_choice["l_val"] == '':
            new_user = models.Child(master = 0, leverage_type = user_choice["leverage_type"] , leverage_value = None , master_id = int(user_choice["selected_master"]))
        else:
            new_user = models.Child(master = 0, leverage_type = user_choice["leverage_type"] , leverage_value = user_choice["l_val"] , master_id = int(user_choice["selected_master"]))
    else:
        new_user = models.User(master = 1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #print(type(user_choice))
    #print("choice is called")
    return {"message": "Hello World"}



# Setting ApiKey in Cookies
@app.get("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value="$2b$12$o7wfxNgH.QFgSSg8lenune9/34VeRRyByi7kqOcWdw.WmATdDUnb6")
    return response

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token", domain='127.0.0.1')
    return response

# Defining a function just to check the function of APIKey
@app.get("/check")
async def checking(request: Request, api_key: APIKey = Depends(get_api_key), response_class=HTMLResponse):
    print("Entering the Checking Function")
    return templates.TemplateResponse('homepage.html', {"request": request})