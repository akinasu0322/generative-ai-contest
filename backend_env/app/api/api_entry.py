from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import pytz
from functools import wraps
from ulid import ULID
from app.db.db_tools import get_db_cursor
from app.api.analyze import analyzer
from app.api.summary import create_summary
from app.api.gen_question import function_for_get_question, function_for_post_answer, factor_arr
# from flask_swagger import swagger

TIME_ZONE = pytz.timezone("Asia/Tokyo")
TIMEOUT_HOUR = 1
PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME
app.config["SECRET_KEY"] = "Gen-ai-contest-password"


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
    user_name = user.get("name")

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if role=="user":
        user_id = user["user_id"]
    elif role=="doctor":
        user_id = user["doctor_id"]
    else:
        print(f"Error in login API. Invalid \"role\"={role}")
        exit(0)

    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.now(TIME_ZONE) + timedelta(hours=TIMEOUT_HOUR)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"jwt_token": token, "user_id": user_id, "user_name": user_name}), 200

# 担当患者の追加
@app.route("/register_in_charge_user", methods=["POST"])
@token_required
def register_in_charge_user(current_doctor):
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "user's email is required"}), 400

    with get_db_cursor() as cursor:
        cursor.execute("""
            UPDATE users 
            SET doctor_id = %s 
            WHERE email = %s
            """, 
            (current_doctor, email)
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


    print(period_start)
    print(period_end)
    print(recent_k)
    print(user_id)
    if not records:
        return jsonify([]), 200

    record_list = []
    for record in records:
        record_list.append({
            "date": record["created_time"],
            "trigger": {
                "environment": {
                    "strong_light": bool(record["strong_light"]),
                    "unpleasant_odor": bool(record["unpleasant_odor"]),
                    "took_bath": bool(record["took_bath"]),
                    "weather_change": bool(record["weather_change"]),
                    "temperture_change": bool(record["temperture_change"]),
                    "crowds": bool(record["crowds"])
                },
                "food": {
                    "dairy_products": bool(record["dairy_products"]),
                    "alcohol": bool(record["alcohol"]),
                    "smoked_fish": bool(record["smoked_fish"]),
                    "nuts": bool(record["nuts"]),
                    "chocolate": bool(record["chocolate"]),
                    "chinese_food": bool(record["chinese_food"])
                },
                "hormone": {
                    "menstruation": bool(record["menstruation"]),
                    "pill_taken": bool(record["pill_taken"])
                },
                "physical": {
                    "body_posture": bool(record["body_posture"]),
                    "carried_heavy_object": bool(record["carried_heavy_object"]),
                    "intense_exercise": bool(record["intense_exercise"]),
                    "long_driving": bool(record["long_driving"]),
                    "travel": bool(record["travel"]),
                    "sleep": bool(record["sleep"]),
                    "toothache": bool(record["toothache"]),
                    "neck_pain": bool(record["neck_pain"]),
                    "hypertension": bool(record["hypertension"]),
                    "shock": bool(record["shock"]),
                    "stress": bool(record["stress"])
                }
            },
            "status": {
                "headache_intensity": bool(record["headache_intensity"]),
                "medicine_taken": bool(record["medicine_taken"]),
                "medicine_effect": bool(record["medicine_effect"]),
                "medicine_name": record["medicine_name"]
            }
        })
    print(record_list)
    return jsonify(record_list), 200


# チャットの開始
@app.route("/start_chat", methods=["POST"])
@token_required
def start_chat(current_user):
    chat_id = str(ULID())
    record_id = str(ULID())
    data = request.get_json()
    call_time = data.get('call_time')
    # created_time = datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H') if call_time=='0000-00-00-00' else call_time
    created_time = datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H') 

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO chat_logs (chat_id, user_id, record_id, created_time) 
            VALUES (%s, %s, %s, %s)
            """, 
            (chat_id, current_user, record_id, created_time)
        )

    # セッション
    session["chat_id"] = chat_id
    session["question_count"] = 0
    session["answer_count"] = 0
    session["pre_question_history_id"] = "new"
    session["prompt_prefix"] = "偏頭痛患者に偏頭痛の要因の有無を訊く30字程度の質問を生成してください．要因として考えられるものは以下のとおりです．\n"
    session["factor_unused_list"] = [True for _ in range(len(factor_arr))]
    session.permanent = True
    session.modified = True

    return jsonify({"chat_id": chat_id}), 201


# 質問の生成
@app.route("/gen_question", methods=["POST"])
@token_required
def gen_question(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    question_id = str(ULID())

    print("session's chat_id")
    print(session["chat_id"])
    print("payload chat_id")
    print(chat_id)
    
    assert(session["chat_id"]==chat_id)
    index_in_chat = session["question_count"]

    # 204を返す
    if session["question_count"] == 5:
        return jsonify({"question": None, "question_id": None}), 204
    
    # TODO: 次に行うべき質問を生成するロジックの実装
    pre_question_history_id = session["pre_question_history_id"]
    prompt_prefix = session["prompt_prefix"]
    factor_unused_list = session["factor_unused_list"]
    question, next_pre_question_history_id = function_for_get_question(factor_unused_list=factor_unused_list, history_id=pre_question_history_id, prompt_prefix=prompt_prefix)
    session["pre_question_history_id"] = next_pre_question_history_id
    target_trigger = f"headache_intensity" # backend側で決定

    # データベースの更新
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO questions (question_id, chat_id, question, target_trigger, created_time, index_in_chat) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, 
            (question_id, chat_id, question, target_trigger, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'), index_in_chat)
        )

    # セッション情報の更新
    session["question_count"] += 1
    session.modified = True

    return jsonify({"question": question, "question_id": question_id}), 200


# 回答の送信
@app.route("/post_answer", methods=["POST"])
@token_required
def post_answer(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    question_id = data.get("question_id")

    assert(session["chat_id"]==chat_id)

    # TODO: answerの解析を行い、それに基づいてuser_recordを更新するロジックを実装する。
    answer = data.get("answer")

    # データベースの更新
    with get_db_cursor() as cursor:
        cursor.execute("""
            UPDATE questions 
            SET answer = %s 
            WHERE question_id = %s
            """, 
            (answer, question_id)
        )

    # セッション情報の更新
    session["answer_count"] += 1
    session["prompt_prefix"] = function_for_post_answer(answer)
    session.modified = True

    return jsonify({"message": "Answer submitted successfully"}), 200


# サマリーの生成
@app.route("/gen_summary", methods=["POST"])
@token_required
def gen_summary(current_user):
    data = request.get_json()
    chat_id = data.get("chat_id")
    summary_id = str(ULID())
    user_id = current_user

    assert(session["chat_id"]==chat_id)
    
    # サマリーの作成
    summary = create_summary(chat_id)
    print(summary)

    # サマリーの登録
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
    
    # アナライズ結果の生成
    analyze_result = analyzer(chat_id)
    print(analyze_result)

    # データベースへの結果の登録
    with get_db_cursor() as cursor:
        # usersテーブルからmedicine_nameを取得
        cursor.execute("""
            SELECT medicine_name
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)  # user_idを指定して薬の名前を取得
        )
        result = cursor.fetchone()
        medicine_name = result["medicine_name"]

        # chat_logsテーブルから最新のcreated_timeとrecord_idを取得
        cursor.execute("""
            SELECT created_time, record_id
            FROM chat_logs
            WHERE chat_id = %s
            ORDER BY created_time DESC
            LIMIT 1
            """,
            (chat_id,)  # chat_idを指定して最新の作成日時を取得
        )
        response = cursor.fetchone()
        created_time = response["created_time"]
        print(f"created_time{created_time}")
        record_id = response["record_id"]

    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_record (
                record_id, user_id, created_time, strong_light, unpleasant_odor, took_bath, 
                weather_change, temperture_change, crowds, dairy_products, alcohol, smoked_fish, 
                nuts, chocolate, chinese_food, menstruation, pill_taken, body_posture, 
                carried_heavy_object, intense_exercise, long_driving, travel, sleep, 
                toothache, neck_pain, hypertension, shock, stress, headache_intensity, 
                medicine_taken, medicine_effect, medicine_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                record_id, user_id, created_time, 
                analyze_result.get("strong_light", None), 
                analyze_result.get("unpleasant_odor", None), 
                analyze_result.get("took_bath", None), 
                analyze_result.get("weather_change", None), 
                analyze_result.get("temperture_change", None), 
                analyze_result.get("crowds", None), 
                analyze_result.get("dairy_products", None), 
                analyze_result.get("alcohol", None), 
                analyze_result.get("smoked_fish", None), 
                analyze_result.get("nuts", None), 
                analyze_result.get("chocolate", None), 
                analyze_result.get("chinese_food", None), 
                analyze_result.get("menstruation", None), 
                analyze_result.get("pill_taken", None), 
                analyze_result.get("body_posture", None), 
                analyze_result.get("carried_heavy_object", None), 
                analyze_result.get("intense_exercise", None), 
                analyze_result.get("long_driving", None), 
                analyze_result.get("travel", None), 
                analyze_result.get("sleep", None), 
                analyze_result.get("toothache", None), 
                analyze_result.get("neck_pain", None), 
                analyze_result.get("hypertension", None), 
                analyze_result.get("shock", None), 
                analyze_result.get("stress", None), 
                analyze_result.get("headache_intensity", None), 
                analyze_result.get("medicine_taken", None), 
                analyze_result.get("medicine_effect", None), 
                medicine_name
            )
        )

    return jsonify({"summary": summary}), 200


# Mibs4とHit6の結果を記録
# TODO: 任意のアンケートの記録をできるようにする。現状mibs4とhit6にしか対応していない。
@app.route("/post_questionnaire_result", methods=["POST"])
@token_required
def post_questionnaire_result(current_user):
    data = request.get_json()
    questionnaire_title = data.get("questionnaire_title")
    answers = data.get("answer")

    if questionnaire_title == "mibs4":
        table = "mibs4"
        query = """
            INSERT INTO mibs4 (user_id, created_time, question1, question2, question3, question4) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (current_user, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'), *answers)
    elif questionnaire_title == "hit6":
        table = "hit6"
        query = """
            INSERT INTO hit6 (user_id, created_time, question1, question2, question3, question4, question5, question6) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (current_user, datetime.now(TIME_ZONE).strftime('%Y-%m-%d-%H'), *answers)
    else:
        return jsonify({"error": "Invalid questionnaire title"}), 400

    with get_db_cursor() as cursor:
        cursor.execute(query, params)

    return jsonify({"message": "Questionnaire result recorded successfully"}), 201



# アンケートの回答を取得
@app.route("/get_questionnaire_result", methods=["POST"])
@token_required
def get_questionnaire_result(current_user):
    data = request.get_json()
    print(data)
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


# # OpenAPI定義を取得するためのAPI
# @app.route("/swagger")
# def swagger_spec():
#     return jsonify(swagger(app))


if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host="0.0.0.0", port=5000, debug=True)