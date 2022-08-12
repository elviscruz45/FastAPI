#python
from typing import Optional                                 #5 tipado estatico
from enum import Enum

#Pydantic                                                   
from pydantic import BaseModel                              #4 sirve para crear modelos
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query ,Path,Form , Header, Cookie, UploadFile,File


app=FastAPI() #1. se instancia fast API

#Models
class HairColor(Enum):
    white= "white",
    brown="brown"
    black="black"
    blonde="blonde"
    red="red"

class PersonBase(BaseModel):
    first_name:str= Field(
    ...,
    min_length=1,
    max_length=50,
        example="Elvis"
    )
    last_name:str= Field(
        ...,
        min_length=1,
        max_length=50,
        example="Cruz"

    )
    age:int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    
    hair_color:Optional[HairColor]=Field(default=None,example="black")
    is_married: Optional[bool]=Field(defaul=None,example=False)

class Location(BaseModel):
    city:str 
    state: str
    country:str

class Person(PersonBase):                                    #Creamos un modelo de persona
    password:str=Field(...,min_length=8)

class PersonOut(PersonBase):
    pass
    
class LoginOut(BaseModel):
    username: str=Field(...,max_length=20,example="elviscruz45")
    message:str=Field(default="login Successfully!")



@app.get(path="/",
         status_code=status.HTTP_200_OK)                                                   #2 metodo get del objeto app, get es una funcion que decorara
def home():                                                     #3 la funcion que se trabajara
    return {"Hello":"World"}

# Request and Response Body

@app.post(path="/person/new",
          response_model=PersonOut,
          status_code=status.HTTP_201_CREATED,
          tags=["Persons"],
          summary="Create Person in the app")                                        # Estamos intentando crear una persona
def create_person(person:Person=Body(...)):
    """
    Create Person
    
    This path operation creates a person in the appp and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person:Person** -> A person model with first name, last name , age, hair color and marital status
        
    Returns a person model with first name , last name, lasta name, age, hair color and marital status
    """
    return person

# Validaciones : Query Parameters
@app.get(path="/person/detail",
         status_code=status.HTTP_200_OK,
         tags=["Persons"],
         deprecated=True)
def show_person(
    name:Optional[str]=Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's betwwn 1 and 50 characters",
        example="Rocio"
        ),
    age:str=Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
):
    return {name:age}

#Validaciones : Path Parameters
persons=[1,2,3,4,5]

@app.get(path="/person/detail/{person_id}",
         tags=["Persons"])
def show_person(
    person_id: int=Path(
        ...,
        gt=0,
        example=123
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: "It exists!"}

#Validaciones: Request Body
@app.put(path="/person/{person_id}",
         tags=["Persons"])
def update_person(
    person_id: int=Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person=Body(...),
):

    return person


#Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username: str=Form(...), password:str=Form(...)):
    return LoginOut(username=username)


#Cookies and headers parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str=Form(
        ...,
        max_length=20,
        min_length=1
),
    last_name: str=Form(
        ...,
        max_length=20,
        min_length=1         
),
    email:EmailStr=Form(...),
    message: str=Form(...,min_length=20),
    user_agent:Optional[str]=Header(default=None),
    ads: Optional[str]=Cookie(default=None)
    ):
    return user_agent

# Files

@app.post(
    path="/post-image"
)
def post_image(
    image:UploadFile=File(...)
):
    return{
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
    }

