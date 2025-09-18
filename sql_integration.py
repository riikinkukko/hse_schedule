import sqlite3
from pathlib import Path
from config import DB_PATH

def get_connection(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def add_user(user_id: int, tg_id: int, coordinates: tuple[float, float], transport: str):
    with get_connection(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, tg_id, latitude, longtitude, transport)
            VALUES (?, ?, ?, ?, ?)''', (user_id, tg_id, coordinates[0], coordinates[1], transport))
        con.commit()

def update_coordinates(tg_id, coordinates: tuple[float, float]):
    with get_connection(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute('''
            UPDATE users
            SET latitude = ?, longitude = ?
            WHERE tg_id = ?''', (coordinates[0], coordinates[1], tg_id))
        con.commit()

def update_transport(tg_id: int, coordinates: tuple[float, float]):
    with get_connection(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute('''
            UPDATE users
            SET latitude = ?, longitude = ?
            WHERE id = ?''', (coordinates[0], coordinates[1], tg_id))
        con.commit()

def get_user(tg_id: int) -> dict:
    with get_connection(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "latitude": row[1], "longitude": row[2], "transport": row[3]}
        raise Exception("Пользователя с таким tg_id нет")

def get_coordinates(tg_id: int):
    response = get_user(tg_id)
    return (response["latitude"], response["longtitude"])

def get_transport(tg_id: int):
    response = get_user(tg_id)
    return (response["transport"])