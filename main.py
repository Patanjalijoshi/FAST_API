from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [  
    User(
        id=uuid4(),
        first_name="Ram",
        last_name="sham",
        gender=Gender.male,
        roles=[Role.student]
    ),
    User(
        id=uuid4(),
        first_name="abc",
        last_name="def",
        gender=Gender.female,
        roles=[Role.admin]
    ),
    User(
        id=uuid4(),
        first_name="qwe",
        last_name="rty",
        gender=Gender.male,
        roles=[Role.teacher, Role.admin]
    )
]

@app.get("/")
async def root():
    return {"Hello": "patanjali"}

@app.get("/api/v1/user")
async def fetch_users():
    return db

@app.post("/api/v1/user")
async def register_user(user: User):
    user.id = uuid4()  # Generate a new ID for the user
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/user/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )

@app.put("/api/v1/user/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )
