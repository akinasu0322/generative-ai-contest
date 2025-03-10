import os
from app.db.db_tools import get_db_cursor
import csv


# テーブルの内容をTSVファイルに保存する関数
def export_tables_to_tsv():
    # tmpフォルダが存在しない場合は作成
    if not os.path.exists('tmp'):
        os.makedirs('tmp')


    with get_db_cursor() as cursor:
        # データベース内のすべてのテーブル名を取得
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()


        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # TSVファイルに保存
            tsv_file_path = os.path.join('tmp', f"{table_name}.tsv")
            with open(tsv_file_path, 'w', newline='', encoding='utf-8') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                writer.writerow(columns)  # ヘッダー行の書き込み
                formated_rows = [[row[column] for column in columns] for row in rows]
                writer.writerows(formated_rows)  # データ行の書き込み

            print(f"Exported {table_name} to {tsv_file_path}")


# メイン関数
if __name__ == "__main__":
    export_tables_to_tsv()
