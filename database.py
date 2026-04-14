import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='app.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Анализы
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            date TIMESTAMP,
            type TEXT
        )
        """)

        # Изображения
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER,
            filename TEXT,
            upload_date TIMESTAMP,
            path TEXT,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id)
        )
        """)

        # Объекты
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
        """)

        # Результаты
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id INTEGER,
            object_id INTEGER,
            x INTEGER,
            y INTEGER,
            probability REAL,
            fragment_path TEXT,
            FOREIGN KEY (image_id) REFERENCES images(id),
            FOREIGN KEY (object_id) REFERENCES objects(id)
        )
        """)

        self.conn.commit()

    # Анализ
    def create_analysis(self, description="Анализ"):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO analyses (description, date, type)
            VALUES (?, ?, ?)
        """, (description, datetime.now(), "image"))
        self.conn.commit()
        return cursor.lastrowid

    # Изображение
    def add_image(self, analysis_id, filename, path):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO images (analysis_id, filename, upload_date, path)
            VALUES (?, ?, ?, ?)
        """, (analysis_id, filename, datetime.now(), path))
        self.conn.commit()
        return cursor.lastrowid

    # Объект
    def add_object(self, name, description=""):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO objects (name, description)
            VALUES (?, ?)
        """, (name, description))
        self.conn.commit()
        return cursor.lastrowid

    # Результат
    def add_result(self, image_id, object_id, x, y, probability, fragment_path):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO results (image_id, object_id, x, y, probability, fragment_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (image_id, object_id, x, y, probability, fragment_path))
        self.conn.commit()