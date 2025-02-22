from fastapi import FastAPI,Path,Body, Header, Cookie, Depends, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from random import randrange

from typing import Annotated, Literal

fake_users_db = {
    "john": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int=Field(0,gt=0,le=100)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

app = FastAPI()

items = []

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    #print(form_data.username, form_data.password)
    user_dict = fake_users_db.get(form_data.username)
    #print(user_dict)
    if not user_dict:
        #print('I am raised...')
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        #print('Password exception raised')
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/")
async def home():
    return {"message":"Hello This is FastAPI home page."}

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    for item in items:
        if item["user_id"] == item_id:
            return item
        
    return {"message":"invalid user id"}

@app.put("/item/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    user: User | None = None,
    item:FilterParams=None,
    imp:int=Body()
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"User":user})
    if imp:
        results.update({"importance":imp})
    return results

@app.get("/get/")
async def get_query(x_value:list[str]=Header(), cook:str=Cookie()):
    return {"Your Hader":x_value, "Your Cookie":cook}


@app.post("/create")
async def create(user:User):
    id = randrange(1,1000)
    items.append({"user_id":id, **user.model_dump()})
    return {"user_id":id, **user.model_dump()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: User, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result