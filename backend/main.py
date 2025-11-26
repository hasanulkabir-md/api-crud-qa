from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

DB_PATH = "crud.db"

app = FastAPI()

# ---------- DB SETUP ----------

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

# ---------- MODELS ----------

class User(BaseModel):
    name: str
    email: str

# ---------- ROUTES ----------

@app.get("/")
def root():
    return {"message": "API is running. See /docs for documentation."}

@app.post("/users/")
def create_user(user: User):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        conn.commit()
        user_id = cur.lastrowid
        return {"message": "User created", "id": user_id}
    except sqlite3.IntegrityError:
        # This is ONLY raised for UNIQUE / NOT NULL violations
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

@app.get("/users/")
def list_users():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "name": row[1], "email": row[2]}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (user.name, user.email, user_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
