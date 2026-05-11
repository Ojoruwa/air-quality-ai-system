import sqlite3
from datetime import datetime

DB_NAME = "air_quality.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        pm10 REAL,
        pm25 REAL,
        no2 REAL,
        so2 REAL,
        o3 REAL,
        temperature REAL,
        humidity REAL,
        windspeed REAL,
        prediction INTEGER
    )
    """)

    conn.commit()
    conn.close()


def save_prediction(data, prediction):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            timestamp, pm10, pm25, no2, so2, o3,
            temperature, humidity, windspeed, prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        data["PM10"],
        data["PM2_5"],
        data["NO2"],
        data["SO2"],
        data["O3"],
        data["Temperature"],
        data["Humidity"],
        data["WindSpeed"],
        prediction
    ))

    conn.commit()
    conn.close()