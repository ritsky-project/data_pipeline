import psycopg2
from api_request import mock_fetch_data

def connect_to_db():
    print("connecting to PostgreSQL database.....")
    try : 
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="WeatherDW",
            user="ritik",
            password="secret123"
        )
        return conn
    except psycopg2.Error as e :
        print(f"Database connection faild : {e}")
        raise

def create_table(conn):
    print("Creating table if not exists")
    try:
        cursor = conn.cursor()

        cursor.execute("CREATE SCHEMA IF NOT EXISTS weather;")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather.api_weather_data(
                id SERIAL PRIMARY KEY,
                city VARCHAR(150),
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_date TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
            """
        )

        conn.commit()
        cursor.close()
        print("Table was created successfully")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Failed to create table: {e}")
        raise

conn = connect_to_db()
create_table(conn)
