import psycopg2
from api_request import mock_fetch_data

def connect_to_db():
    print("connecting to PostgreSQL database.....")
    try:
        conn = psycopg2.connect(
            host="postgres",   # FIX THIS
            port=5432,
            dbname="WeatherDW",
            user="ritik",
            password="secret123"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS weather;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather.api_weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(150),
            temperature FLOAT,
            weather_description TEXT,
            wind_speed FLOAT,
            humidity FLOAT,
            time TIMESTAMP,
            utc_offset TEXT,
            inserted_date TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()

def insert_record(conn, data):
    weather = data['current']
    location = data['location']
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO weather.api_weather_data(
            city, temperature, weather_description,
            wind_speed, humidity, time, inserted_date, utc_offset
        ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
    """, (
        location['name'],
        weather['temperature'],
        weather['weather_descriptions'][0],
        weather['wind_speed'],
        weather['humidity'],
        location['localtime'],
        location['utc_offset']
    ))

    conn.commit()

def main():
    conn = None
    try:
        data = mock_fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_record(conn, data)
    except Exception as e:
        print(f"Execution failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            print("Connection closed")