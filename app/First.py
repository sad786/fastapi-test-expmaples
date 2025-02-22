from enum import Enum
from typing import Annotated
from fastapi import Form
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

#app = FastAPI()
app = FastAPI(
    title="My First API"
)

@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

#app = FastAPI()

class ModelName(int,Enum):
    alexnet = 10
    resnet = 11
    lenet = 12

class User(BaseModel):
    name:str
    age:int

class FormModel(BaseModel):
    username:str
    password:str

@app.post("/login/")
async def login(user:Annotated[FormModel, Form(title="insert username and password")]):
    return user

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.post("/post")
async def get_post(data:User):
    return {'Hello ':data.name, 'message': 'Hello Bhai where you today you age is '+str(data.age)}
