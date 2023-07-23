from uuid import uuid4
from fastapi import FastAPI
from typing import List
from models import User, Gender, Role

app = F astAPI()

db: List[User] = [  
      
    User(
        id=uuid4(),
        first_name="Ram",
        last_name="sham",
        gender= Gender.male,
        roles= [Role.student]    
    ),
    User(
        id=uuid4(),
        first_name="abc",
        last_name="def",
        gender= Gender.female,
        roles= [Role.admin]    
    ),
    User(
        id=uuid4(),
        first_name="qwe",
        last_name="rty",
        gender= Gender.male,
        roles= [Role.teacher, Role.admin]    
    )
]
@app.get("/")

async def root():
    return {"Hello": "patanjali"}

@app.get("/api/v1/user")
async def fetch_users():
        return db