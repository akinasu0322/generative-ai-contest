import mysql.connector
import os
from contextlib import contextmanager

# データベース接続
def get_db_connection():
    connection = mysql.connector.connect(
        host = os.getenv("RDS_END_POINT"),
        user = os.getenv("RDS_USER") ,
        password = os.getenv("RDS_PASS"),
        database = os.getenv("RDS_DB_NAME")
    )
    return connection

# カーソルの生成
@contextmanager
def get_db_cursor():
    connection = get_db_connection()  # 既存の接続取得関数を使う
    cursor = connection.cursor(dictionary=True)
    
    try:
        yield cursor  # カーソルを返す
    finally:
        # 終わったらカーソルと接続を自動で閉じる
        connection.commit()
        cursor.close()
        connection.close()

