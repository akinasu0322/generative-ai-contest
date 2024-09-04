import os
import mysql.connector
from dotenv import load_dotenv
import csv

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

# テーブルの内容をTSVファイルに保存する関数
def export_tables_to_tsv():
    connection = get_db_connection()
    cursor = connection.cursor()

    # tmpフォルダが存在しない場合は作成
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # データベース内のすべてのテーブル名を取得
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # TSVファイルに保存
        tsv_file_path = os.path.join('tmp', f"{table_name}.tsv")
        with open(tsv_file_path, 'w', newline='', encoding='utf-8') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow(columns)  # ヘッダー行の書き込み
            writer.writerows(rows)  # データ行の書き込み

        print(f"Exported {table_name} to {tsv_file_path}")

    cursor.close()
    connection.close()

# メイン関数
if __name__ == "__main__":
    export_tables_to_tsv()
