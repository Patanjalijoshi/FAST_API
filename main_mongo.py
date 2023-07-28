import pymongo
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["school"]
users_collection = db["users"]

def insert_initial_data():
    # Sample data to be inserted into the "users" collection
    users_data = [
        {
            "id": str(uuid4()),
            "first_name": "Ram",
            "last_name": "Sham",
            "gender": Gender.male.value,
            "roles": [role.value for role in [Role.student]]
        },
        {
            "id": str(uuid4()),
            "first_name": "abc",
            "last_name": "def",
            "gender": Gender.female.value,
            "roles": [role.value for role in [Role.admin]]
        },
        {
            "id": str(uuid4()),
            "first_name": "qwe",
            "last_name": "rty",
            "gender": Gender.male.value,
            "roles": [role.value for role in [Role.teacher, Role.admin]]
        }
    ]

    users_collection.insert_many(users_data)

# Call the function to insert the initial data during the app startup
insert_initial_data()

@app.get("/")
async def root():
    return {"Hello": "patanjali"}

@app.get("/api/v1/user")
async def fetch_users():
    users = list(users_collection.find())
    return users

@app.post("/api/v1/user")
async def register_user(user: User):
    user_data = {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name,
        "gender": user.gender.value,
        "roles": [role.value for role in user.roles]
    }
    users_collection.insert_one(user_data)
    return {"id": user.id}

@app.delete("/api/v1/user/{user_id}")
async def delete_user(user_id: UUID):
    result = users_collection.delete_one({"id": str(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exist")

@app.put("/api/v1/user/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    user = users_collection.find_one({"id": str(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exist")
    if user_update.first_name is not None:
        user["first_name"] = user_update.first_name
    if user_update.last_name is not None:
        user["last_name"] = user_update.last_name
    if user_update.middle_name is not None:
        user["middle_name"] = user_update.middle_name
    if user_update.roles is not None:
        user["roles"] = [role.value for role in user_update.roles]

    users_collection.replace_one({"id": str(user_id)}, user)
    return user
