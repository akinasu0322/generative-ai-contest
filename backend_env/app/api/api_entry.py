from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import pytz
from functools import wraps
from ulid import ULID
from app.db.db_tools import get_db_cursor

app = Flask(__name__)
app.config["SECRET_KEY"] = "Gen-ai-contest-password"
TIME_ZONE = pytz.timezone("Asia/Tokyo")
TIMEOUT_HOUR = 1

# ユーザー認証
def authenticate_user(email, password, role):
    with get_db_cursor() as cursor:
        if role == "user":
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        else:
            cursor.execute("SELECT * FROM doctors WHERE email = %s", (email,))
        user = cursor.fetchone()

    if user and check_password_hash(user["hashed_password"], password):
        return user
    return None

# トークン認証デコレータ
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1]  # "Bearer <token>" の形式を想定
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user_id"]
        except Exception as e:
            return jsonify({"error": "Invalid token!"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


############## API ###################
# ユーザー情報の登録
@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.get_json()

    user_id = str(ULID())
    email = data.get("email")
    username = data.get("user_name")
    password = data.get("password")
    age = data.get("age")
    sex = data.get("sex")
    prefecture = data.get("prefecture")
    medicine_name = data.get("medicine_name")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO users 
            (user_id, email, name, hashed_password, age, sex, prefecture, medicine_name) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (user_id, email, username, hashed_password, age, sex, prefecture, medicine_name)
        )

    return jsonify({"user_id": user_id, "message": "User registered successfully"}), 201


# 医者情報の登録
@app.route("/register_doctor", methods=["POST"])
def register_doctor():
    data = request.get_json()

    doctor_id = str(ULID())
    email = data.get("email")
    username = data.get("user_name")
    password = data.get("password")
    age = data.get("age")
    sex = data.get("sex")
    hospital_id = data.get("hospital_id")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO doctors 
            (doctor_id, email, name, hashed_password, age, sex, hospital_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, 
            (doctor_id, email, username, hashed_password, age, sex, hospital_id)
        )

    return jsonify({"doctor_id": doctor_id, "message": "Doctor registered successfully"}), 201


# 病院情報の登録
@app.route("/register_hospital", methods=["POST"])
def register_hospital():
    data = request.get_json()

    hospital_id = str(ULID())
    hospital_name = data.get("hospital_name")
    hospital_code = data.get("hospital_code")
    password = data.get("password")

    if not hospital_name or not password:
        return jsonify({"error": "Hospital name and password are required"}), 400

    hashed_password = generate_password_hash(password)

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO hospitals 
            (hospital_id, name, hashed_password) 
            VALUES (%s, %s, %s)
            """, 
            (hospital_id, hospital_name, hashed_password)
        )

    return jsonify({"hospital_id": hospital_id, "message": "Hospital registered successfully"}), 201


# ログイン
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # "user" か "doctor" を指定

    user = authenticate_user(email, password, role)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user_id": user["user_id"],
            "exp": datetime.now(TIME_ZONE) + timedelta(hours=TIMEOUT_HOUR)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"jwt_token": token}), 200

# 担当患者の追加
@app.route("/register_in_charge_user", methods=["POST"])
@token_required
def register_in_charge_user(current_doctor):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    with get_db_cursor() as cursor:
        cursor.execute("""
            UPDATE users 
            SET doctor_id = %s 
            WHERE user_id = %s
            """, 
            (current_doctor, user_id)
        )

    return jsonify({"message": "User assigned to doctor successfully"}), 200


# 担当患者の情報取得
@app.route("/get_in_charge_users_info", methods=["GET"])
@token_required
def get_in_charge_users_info(current_doctor):
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT u.user_id, u.name, u.email, r.headache_intensity, r.medicine_taken, r.medicine_effect, r.medicine_name 
            FROM users u 
            LEFT JOIN user_record r ON u.user_id = r.user_id
            WHERE u.doctor_id = %s AND r.created_time = (
                SELECT MAX(created_time) FROM user_record WHERE user_id = u.user_id
            )
            """, 
            (current_doctor,)
        )
        users = cursor.fetchall()

    if not users:
        return jsonify({"error": "No users found for this doctor"}), 404

    user_info = []
    for user in users:
        user_info.append({
            "user_id": user["user_id"],
            "user_name": user["name"],
            "user_email": user["email"],
            "status": {
                "headache_intensity": user["headache_intensity"],
                "medicine_taken": bool(user["medicine_taken"]),
                "medicine_effect": user["medicine_effect"],
                "medicine_name": user["medicine_name"]
            }
        })

    return jsonify(user_info), 200


# ユーザー情報の取得
@app.route("/get_user_info", methods=["POST"])
@token_required
def get_user_info(current_user):
    data = request.get_json()
    user_id = data.get("user_id")
    period_start = data.get("period_start")
    period_end = data.get("period_end")
    recent_k = data.get("recent_k")

    query = """
        SELECT * FROM user_record 
        WHERE user_id = %s 
        """
    params = [user_id]

    if period_start and period_end:
        query += "AND created_time BETWEEN %s AND %s "
        params.extend([period_start, period_end])

    query += "ORDER BY created_time DESC "

    if recent_k:
        query += "LIMIT %s"
        params.append(recent_k)

    with get_db_cursor() as cursor:
        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

    if not records:
        return jsonify({"error": "No records found"}), 404

    record_list = []
    for record in records:
        record_list.append({
            "date": record["created_time"],
            "trigger": {
                "environment": {
                    "strong_light": record["strong_light"],
                    "unpleasant_odor": record["unpleasant_odor"],
                    "took_bath": record["took_bath"],
                    "weather_change": record["weather_change"],
                    "temperture_change": record["temperture_change"],
                    "crowds": record["crowds"]
                },
                "food": {
                    "dairy_products": record["dairy_products"],
                    "alcohol": record["alcohol"],
                    "smoked_fish": record["smoked_fish"],
                    "nuts": record["nuts"],
                    "chocolate": record["chocolate"],
                    "chinese_food": record["chinese_food"]
                },
                "hormone": {
                    "menstruation": record["menstruation"],
                    "pill_taken": record["pill_taken"]
                },
                "physical": {
                    "body_posture": record["body_posture"],
                    "carried_heavy_object": record["carried_heavy_object"],
                    "intense_exercise": record["intense_exercise"],
                    "long_driving": record["long_driving"],
                    "travel": record["travel"],
                    "sleep": record["sleep"],
                    "toothache": record["toothache"],
                    "neck_pain": record["neck_pain"],
                    "hypertension": record["hypertension"],
                    "shock": record["shock"],
                    "stress": record["stress"]
                }
            },
            "status": {
                "headache_intensity": record["headache_intensity"],
                "medicine_taken": record["medicine_taken"],
                "medicine_effect": record["medicine_effect"],
                "medicine_name": record["medicine_name"]
            }
        })

    return jsonify(record_list), 200


# チャットの開始
@app.route("/start_chat", methods=["POST"])
@token_required
def start_chat(current_user):
    chat_id = str(ULID())
    record_id = str(ULID())
    created_time = datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H')

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO chat_logs (chat_id, user_id, record_id, created_time) 
            VALUES (%s, %s, %s, %s)
            """, 
            (chat_id, current_user, record_id, created_time)
        )
        cursor.execute("""
            INSERT INTO user_record (record_id, user_id, created_time) 
            VALUES (%s, %s, %s)
            """, 
            (record_id, current_user, created_time)
        )

    return jsonify({"chat_id": chat_id}), 201


# 質問の生成
@app.route("/gen_question", methods=["POST"])
@token_required
def gen_question(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    question_id = str(ULID())
    question = f"本日、頭痛の症状はどうでしたか？"

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions (question_id, chat_id, question, created_time) 
            VALUES (%s, %s, %s, %s)
            """, 
            (question_id, chat_id, question, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'))
        )

    return jsonify({"question": question, "question_id": question_id}), 200


# 回答の送信
@app.route("/post_answer", methods=["POST"])
@token_required
def post_answer(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    question_id = data.get("question_id")
    answer = data.get("answer")

    # TODO: answerの解析を行い、それに基づいてuser_recordを更新するロジックを実装する。

    with get_db_cursor() as cursor:
        cursor.execute("""
            UPDATE questions 
            SET answer = %s 
            WHERE question_id = %s
            """, 
            (answer, question_id)
        )

    return jsonify({"message": "Answer submitted successfully"}), 200


# サマリーの生成
@app.route("/gen_summary", methods=["POST"])
@token_required
def gen_summary(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    summary_id = str(ULID())
    summary = "チャットのサマリーをここに生成します。"  # TODO: 実際にサマリー生成ロジックを追加

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO summaries (summary_id, summary, created_time) 
            VALUES (%s, %s, %s)
            """, 
            (summary_id, summary, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'))
        )
        cursor.execute("""
            UPDATE chat_logs 
            SET summary_id = %s 
            WHERE chat_id = %s
            """, 
            (summary_id, chat_id)
        )

    return jsonify({"summary": summary}), 200


# Mibs4とHit6の結果を記録
@app.route("/post_questionnaire_result", methods=["POST"])
@token_required
def post_questionnaire_result(current_user):
    data = request.get_json()
    questionnaire_title = data.get("questionnaire_title")
    answers = data.get("answer")

    if questionnaire_title == "mibs4":
        table = "mibs4"
    elif questionnaire_title == "hit6":
        table = "hit6"
    else:
        return jsonify({"error": "Invalid questionnaire title"}), 400

    with get_db_cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO {table} (user_id, created_time, question1, question2, question3, question4) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, 
            (current_user, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'), *answers)
        )

    return jsonify({"message": "Questionnaire result recorded successfully"}), 201


# アンケートの回答を取得
@app.route("/get_questionnaire_result", methods=["POST"])
@token_required
def get_questionnaire_result(current_user):
    data = request.get_json()
    
    user_id = data.get("user_id")
    recent_k = data.get("recent_k", 1)  # デフォルトでは直近1件
    questionnaire_title = data.get("questionnaire_title")

    if questionnaire_title not in ["mibs4", "hit6"]:
        return jsonify({"error": "Invalid questionnaire title"}), 400

    try:
        with get_db_cursor() as cursor:
            if questionnaire_title == "mibs4":
                cursor.execute("""
                    SELECT created_time, question1, question2, question3, question4 
                    FROM mibs4 
                    WHERE user_id = %s 
                    ORDER BY created_time DESC 
                    LIMIT %s
                """, (user_id, recent_k))
            else:
                cursor.execute("""
                    SELECT created_time, question1, question2, question3, question4, question5, question6 
                    FROM hit6 
                    WHERE user_id = %s 
                    ORDER BY created_time DESC 
                    LIMIT %s
                """, (user_id, recent_k))

            results = cursor.fetchall()

        if not results:
            return jsonify({"error": "No results found"}), 404

        # 出力フォーマットの整形
        response = []
        for result in results:
            if questionnaire_title == "mibs4":
                response.append({
                    "date": result["created_time"],
                    "answer": {
                        "question1": result["question1"],
                        "question2": result["question2"],
                        "question3": result["question3"],
                        "question4": result["question4"]
                    }
                })
            else:
                response.append({
                    "date": result["created_time"],
                    "answer": {
                        "question1": result["question1"],
                        "question2": result["question2"],
                        "question3": result["question3"],
                        "question4": result["question4"],
                        "question5": result["question5"],
                        "question6": result["question6"]
                    }
                })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)