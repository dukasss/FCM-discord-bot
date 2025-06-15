# database.py
import sqlite3
import os

DB_FILE = "pocoyo_fcm.db"

def setup_database():
    """Crea las tablas necesarias en la base de datos si no existen."""
    if not os.path.exists(DB_FILE):
        print("Creando archivo de base de datos...")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabla de configuración
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    # Tabla de personajes aprobados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            image_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def set_config(key: str, value: str):
    """Guarda o actualiza una clave de configuración."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_config(key: str) -> int | None:
    """Obtiene un valor de configuración por su clave."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return int(result[0]) if result else None

def add_character(name: str, image_url: str):
    """Añade un nuevo personaje aprobado a la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO characters (name, image_url) VALUES (?, ?)", (name, image_url))
        conn.commit()
    except Exception as e:
        conn.close()
        raise e
    finally:
        conn.close()

def get_random_characters(count: int = 3) -> list[tuple[str, str]]:
    """Selecciona N personajes al azar de la lista de aprobados."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, image_url FROM characters ORDER BY RANDOM() LIMIT ?", (count,))
    results = cursor.fetchall()
    conn.close()
    return results
