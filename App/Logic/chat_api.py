from App.DB.db_tools import get_db_cursor
from ulid import ULID

# チャット開始を知らせる関数
def new_chat(user_id):
    chat_id = str(ULID())  # ULIDでチャットIDを生成
    created_time = "2024/09/06/12"  # 実際には現在時刻を取得
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO chat_log (chat_id, user_id, created_time)
            VALUES (%s, %s, %s)
            """, (chat_id, user_id, created_time)
        )
    return {"chat_id": chat_id}


# 質問生成関数
def gen_question(user_id, chat_id):
    # 質問を仮定して生成
    question_list = [
        "What's your favorite color?",
        "What's your hobby?",
        "Where do you live?",
        "What is your profession?"
    ]
    question = question_list[user_id % len(question_list)]  # ユーザーIDに応じた質問を生成
    question_id = str(ULID())  # ULIDで質問IDを生成
    
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO questions (question_id, question)
            VALUES (%s, %s)
            """, (question_id, question)
        )

    return {"question": question, "question_id": question_id}

# 質問に対する回答送信関数
def post_answer(user_id, chat_id, question_id, answer):
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            UPDATE questions
            SET answer = %s
            WHERE question_id = %s
            """, (answer, question_id)
        )
    return None

# サマリー生成関数（サマリーテーブルの更新）
def gen_summary(user_id, chat_id):
    # 仮のサマリー生成（サマリー）
    summary = f"User {user_id} has completed the chat session."
    summary_id = str(ULID())  # ULIDでサマリーIDを生成

    with get_db_cursor() as cursor:
        # サマリーテーブルに保存
        cursor.execute(
            """
            INSERT INTO summaries (summary_id, summary)
            VALUES (%s, %s)
            """, (summary_id, summary)
        )

        # チャットログテーブルのsummary_idを更新
        cursor.execute(
            """
            UPDATE chat_log
            SET summary_id = %s
            WHERE chat_id = %s
            """, (summary_id, chat_id)
        )

    return {"summary": summary, "summary_id": summary_id}
