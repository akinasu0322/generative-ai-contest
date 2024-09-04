import mysql.connector
import os
from dotenv import load_dotenv

# データベース接続の取得
def get_db_connection():
    load_dotenv()
    connection = mysql.connector.connect(
        host=os.getenv("RDS_END_POINT"),
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASS"),
        database=os.getenv("RDS_DB_NAME")
    )
    return connection

# テーブルを作成する関数
def create_user_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            user_id VARCHAR(26) PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            age INT,
            sex ENUM('male', 'female', 'other'),
            hospital_id VARCHAR(26),
            doctor_id VARCHAR(26)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_weather_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS weather")
    cursor.execute("""
        CREATE TABLE weather (
            date VARCHAR(13) PRIMARY KEY,
            temperature DECIMAL(5, 2),
            pressure DECIMAL(7, 2),
            weather VARCHAR(50),
            wind_direction VARCHAR(50),
            wind_strength VARCHAR(50)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_hospital_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS hospitals")
    cursor.execute("""
        CREATE TABLE hospitals (
            hospital_id VARCHAR(26) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_doctor_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS doctors")
    cursor.execute("""
        CREATE TABLE doctors (
            doctor_id VARCHAR(26) PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            age INT,
            sex ENUM('male', 'female', 'other'),
            hospital_id VARCHAR(26)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_diary_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS diaries")
    cursor.execute("""
        CREATE TABLE diaries (
            diary_id VARCHAR(26) PRIMARY KEY,
            user_id VARCHAR(26),
            text TEXT,
            date VARCHAR(13)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_record_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS user_record")
    cursor.execute("""
        CREATE TABLE user_record (
            record_id VARCHAR(26) PRIMARY KEY,
            user_id VARCHAR(26),
            date VARCHAR(13)
            -- 他の誘発因子カラムをここに追加
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def create_chat_log_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS chat_log")
    cursor.execute("""
        CREATE TABLE chat_log (
            log_id VARCHAR(26) PRIMARY KEY,
            log_order INT,
            role ENUM("user", "assistant", "system"),
            text VARCHAR(2048),
            user_id VARCHAR(26)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()


# メイン関数
if __name__ == "__main__":
    create_user_table()
    create_weather_table()
    create_hospital_table()
    create_doctor_table()
    create_diary_table()
    create_record_table()
    create_chat_log_table()
    print("Tables created successfully.")
