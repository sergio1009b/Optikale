import sqlite3

def crear_db():

    conexion = sqlite3.connect("citas.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS citas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        telefono TEXT NOT NULL,

        gmail TEXT NOT NULL,

        fecha TEXT NOT NULL,

        hora TEXT NOT NULL,

        historia TEXT,

        estado TEXT DEFAULT 'Pendiente'

    )
    """)

    conexion.commit()

    conexion.close()


crear_db()