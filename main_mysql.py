import mysql.connector
from uuid import UUID, uuid4
from fastapi import FastAPI
from typing import List
from models import User, Gender, Role, UserUpdateRequest

def get_mysql_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Jaggu@2023",
        database="school"
    )

app = FastAPI()

# Create the "users" table in the MySQL database if it doesn't exist
with get_mysql_connection() as connection:
    with connection.cursor() as cursor:
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(100),
            gender ENUM('male', 'female') NOT NULL,
            roles VARCHAR(255) NOT NULL
        )
        '''
        cursor.execute(create_table_query)
    connection.commit()

def insert_initial_data():
    # Sample data to be inserted into the "users" table
    users_data = [
        {
            "id": str(uuid4()),
            "first_name": "Ram",
            "last_name": "Sham",
            "gender": Gender.male.value,
            "roles": ','.join([role.value for role in [Role.student]])
        },
        {
            "id": str(uuid4()),
            "first_name": "abc",
            "last_name": "def",
            "gender": Gender.female.value,
            "roles": ','.join([role.value for role in [Role.admin]])
        },
        {
            "id": str(uuid4()),
            "first_name": "qwe",
            "last_name": "rty",
            "gender": Gender.male.value,
            "roles": ','.join([role.value for role in [Role.teacher, Role.admin]])
        }
    ]

    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            insert_query = '''
            INSERT INTO users (id, first_name, last_name, gender, roles)
            VALUES (%(id)s, %(first_name)s, %(last_name)s, %(gender)s, %(roles)s)
            '''

            cursor.executemany(insert_query, users_data)
        connection.commit()

# Call the function to insert the initial data during the app startup
insert_initial_data()


@app.get("/")
async def root():
    return {"Hello": "patanjali"}

@app.get("/api/v1/user")
async def fetch_users():
    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM users'
            cursor.execute(query)
            result = cursor.fetchall()
    return result

@app.post("/api/v1/user")
async def register_user(user: User):
    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            query = '''
            INSERT INTO users (id, first_name, last_name, middle_name, gender, roles)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            values = (str(user.id), user.first_name, user.last_name, user.middle_name, user.gender.value, ','.join(user.roles))
            cursor.execute(query, values)
        connection.commit()
    return {"id": user.id}

@app.delete("/api/v1/user/{user_id}")
async def delete_user(user_id: UUID):
    try:
        with get_mysql_connection() as connection:
            with connection.cursor() as cursor:
                query = 'DELETE FROM users WHERE id = %s'
                cursor.execute(query, (str(user_id),))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist")
                else:
                    return JSONResponse(status_code=200, content={"message": f"User with id: {user_id} has been deleted"})
    except Exception as e:
        # Print or log the exception to check for any errors
        print(f"Error while deleting user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")


@app.put("/api/v1/user/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM users WHERE id = %s'
            cursor.execute(query, (str(user_id),))
            user = cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exist")
            if user_update.first_name is not None:
                user['first_name'] = user_update.first_name
            if user_update.last_name is not None:
                user['last_name'] = user_update.last_name
            if user_update.middle_name is not None:
                user['middle_name'] = user_update.middle_name
            if user_update.roles is not None:
                user['roles'] = ','.join(user_update.roles)
            query = '''
            UPDATE users SET
            first_name = %s,
            last_name = %s,
            middle_name = %s,
            roles = %s
            WHERE id = %s
            '''
            values = (user['first_name'], user['last_name'], user['middle_name'], user['roles'], str(user_id))
            cursor.execute(query, values)
        connection.commit()
    return user
