from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect("crud.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

init_db()

class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
def create_user(user: User):
    try:
        conn = sqlite3.connect("crud.db")
        conn.execute("INSERT INTO users (name,email) VALUES (?,?)", (user.name, user.email))
        conn.commit()
        return {"message": "User created"}
    except:
        raise HTTPException(status_code=400, detail="Email already exists")

@app.get("/users/")
def list_users():
    conn = sqlite3.connect("crud.db")
    rows = conn.execute("SELECT id,name,email FROM users").fetchall()
    return rows

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = sqlite3.connect("crud.db")
    row = conn.execute("SELECT id,name,email FROM users WHERE id=?", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return row

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = sqlite3.connect("crud.db")
    result = conn.execute("UPDATE users SET name=?, email=? WHERE id=?", (user.name, user.email, user_id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = sqlite3.connect("crud.db")
    result = conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
