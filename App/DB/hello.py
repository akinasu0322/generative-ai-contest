import MySQLdb
from datetime import datetime
from dotenv import load_dotenv
import os

# .envファイルの読み込み
load_dotenv()

# RDSへの接続情報
rds_host = os.getenv("RDS_END_POINT")  # RDSのエンドポイント
rds_user = os.getenv("RDS_USER")     # RDSのユーザー名
rds_password = os.getenv("RDS_PASS") # RDSのパスワード
rds_db = os.getenv("RDS_DB_NAME")       # RDSのデータベース名

# RDSに接続
connection = MySQLdb.connect(
    host=rds_host,
    user=rds_user,
    passwd=rds_password,
    db=rds_db,
    charset='utf8'
)

try:
    with connection.cursor() as cursor:
        # テーブルの作成
        create_table_query = """
        CREATE TABLE IF NOT EXISTS diaries (
            diary_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            diary_date DATETIME NOT NULL,
            content TEXT NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()

        # データの挿入
        insert_diary_query = """
        INSERT INTO diaries (user_id, diary_date, content)
        VALUES (%s, %s, %s)
        """
        user_id = 1
        diary_date = datetime.now()
        content = "今日は天気が良く、頭痛が少し和らいだ。"
        cursor.execute(insert_diary_query, (user_id, diary_date, content))
        connection.commit()

        # データの読み取り
        select_query = "SELECT * FROM diaries WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        result = cursor.fetchall()

        for row in result:
            print(f"User ID: {row[0]}, Diary ID: {row[1]}, Date: {row[2]}, Content: {row[3]}")

finally:
    connection.close()
