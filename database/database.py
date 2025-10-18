import sqlite3
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = 'users.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER UNIQUE NOT NULL,
                        group_cst INTEGER,
                        group_eng INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def user_exists(self, tg_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT tg_id FROM users WHERE tg_id = ?', (tg_id,))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False

    def add_user(self, tg_id: int, group_cst: int, group_eng: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (tg_id, group_cst, group_eng)
                    VALUES (?, ?, ?)
                ''', (tg_id, group_cst, group_eng))
                conn.commit()
                logger.info(f"User {tg_id} added successfully")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"User {tg_id} already exists")
            return False
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False

    def get_user_groups(self, tg_id: int) -> Optional[Tuple[int, int]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT group_cst, group_eng FROM users WHERE tg_id = ?', (tg_id,))
                result = cursor.fetchone()
                return result if result else None
        except Exception as e:
            logger.error(f"Error getting user groups: {e}")
            return None

    def update_user_groups(self, tg_id: int, group_cst: int, group_eng: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET group_cst = ?, group_eng = ?
                    WHERE tg_id = ?
                ''', (group_cst, group_eng, tg_id))
                conn.commit()
                logger.info(f"User {tg_id} groups updated successfully")
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating user groups: {e}")
            return False

    def delete_user(self, tg_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE tg_id = ?', (tg_id,))
                conn.commit()
                logger.info(f"User {tg_id} deleted successfully")
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False

db = Database()