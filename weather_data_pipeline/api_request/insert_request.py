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

def insert_record(conn, data) :
    print("Insert Weather Data into database")

    try :
        weather  = data['current']
        location = data['current']
        cursor   = conn.cursor()
        cursor.execute(
            """
            INSERT INTO weather.api_weather_data(
                city,
                temprature,
                weather_description,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            )VALUES(%s, %s, %s, %s, %s ,NOW(), %s)
            """,
            (
                location['name'],
                weather['temprature'],
                weather['weather_description'][0],
                weather['wind_speed'],
                location['localtime'],
                location['utf_offset']
            )
        )
        conn.commit()
        conn.close()
        print("data successfully inserted")
    except psycopg2.Error as e :
        print(f"Error occurred during insertin the data : {e}")


# python weather_data_pipeline/api_request/insert_request.py