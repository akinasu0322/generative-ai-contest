from app.db.db_tools import get_db_cursor


# テーブル作成関数
def create_user_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                user_id VARCHAR(26) PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                age INT,
                sex ENUM('male', 'female', 'other'),
                prefecture VARCHAR(255),
                medicine_name VARCHAR(255),
                hospital_id VARCHAR(26),
                doctor_id VARCHAR(26),
                created_time VARCHAR(13)
            )
        """)
    

def create_weather_table():
    with get_db_cursor() as cursor:
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
    

def create_hospital_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS hospitals")
        cursor.execute("""
            CREATE TABLE hospitals (
                hospital_id VARCHAR(26) PRIMARY KEY,
                hashed_password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL
            )
        """)
    

def create_doctor_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS doctors")
        cursor.execute("""
            CREATE TABLE doctors (
                doctor_id VARCHAR(26) PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                age INT,
                sex ENUM('male', 'female', 'other'),
                hospital_id VARCHAR(26)
            )
        """)
    

def create_diary_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS diaries")
        cursor.execute("""
            CREATE TABLE diaries (
                diary_id VARCHAR(26) PRIMARY KEY,
                user_id VARCHAR(26),
                text TEXT,
                date VARCHAR(13)
            )
        """)
    

def create_record_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS user_record")
        cursor.execute("""
            CREATE TABLE user_record (
                record_id VARCHAR(26) PRIMARY KEY,
                user_id VARCHAR(26),
                created_time VARCHAR(13),
                strong_light TINYINT,
                unpleasant_odor TINYINT,
                took_bath TINYINT,
                weather_change TINYINT,
                temperture_change TINYINT,
                crowds TINYINT,
                dairy_products TINYINT,
                alcohol DECIMAL(2, 1),
                smoked_fish TINYINT,
                nuts TINYINT,
                chocolate TINYINT,
                chinese_food TINYINT,
                menstruation TINYINT,
                pill_taken TINYINT,
                body_posture TINYINT,
                carried_heavy_object TINYINT,
                intense_exercise TINYINT,
                long_driving TINYINT,
                travel TINYINT,
                sleep DECIMAL(2, 1),
                toothache TINYINT,
                neck_pain TINYINT,
                hypertension TINYINT,
                shock TINYINT,
                stress DECIMAL(2, 1),
                headache_intensity DECIMAL(2, 1),
                medicine_taken TINYINT,
                medicine_effect DECIMAL(2, 1),
                medicine_name VARCHAR(255)
            )
        """)
    

def create_chat_log_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS chat_logs")
        cursor.execute("""
            CREATE TABLE chat_logs (
                chat_id VARCHAR(26) PRIMARY KEY,
                user_id VARCHAR(26),
                record_id VARCHAR(26),
                summary_id VARCHAR(26),
                created_time VARCHAR(13)
            )
        """)
    

def create_question_log_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS questions")
        cursor.execute("""
            CREATE TABLE questions (
                question_id VARCHAR(26) PRIMARY KEY,
                chat_id VARCHAR(26),
                question TEXT,
                answer TEXT,
                target_trigger VARCHAR(255),
                created_time VARCHAR(13)
            )
        """)
    

def create_summary_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS summaries")
        cursor.execute("""
            CREATE TABLE summaries (
                summary_id VARCHAR(26) PRIMARY KEY,
                summary TEXT,
                created_time VARCHAR(13)
            )
        """)
    

def create_mibs4_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS mibs4")
        cursor.execute("""
            CREATE TABLE mibs4 (
                user_id VARCHAR(26),
                created_time VARCHAR(13),
                question1 INT,
                question2 INT,
                question3 INT,
                question4 INT
            )
        """)
    

def create_hit6_table():
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS hit6")
        cursor.execute("""
            CREATE TABLE hit6 (
                user_id VARCHAR(26),
                created_time VARCHAR(13),
                question1 INT,
                question2 INT,
                question3 INT,
                question4 INT,
                question5 INT,
                question6 INT
            )
        """)
    

# メイン関数
if __name__ == "__main__":
    create_user_table()
    create_weather_table()
    create_hospital_table()
    create_doctor_table()
    create_diary_table()
    create_record_table()
    create_chat_log_table()
    create_question_log_table()
    create_summary_table()
    create_mibs4_table()
    create_hit6_table()
    print("Tables created successfully.")
