from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import jwt
from datetime import datetime, timedelta
import pytz
import os
from functools import wraps
from ulid import ULID
from app.db.db_tools import get_db_connection, get_db_cursor

app = Flask(__name__)
app.config["SECRET_KEY"] = "Gen-ai-contest-password"
TIME_ZONE = pytz.timezone("Asia/Tokyo")
TIMEOUT_HOUR = 1


# ユーザー認証
def authenticate_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and check_password_hash(user["hashed_password"], password):
        return user
    return None


# jwtトークンのユーザーIDと一致するユーザーIDか確認する処理
def verify_user_id(token, user_id):
    try:
        # トークンの "Bearer <token>" 部分を分割してトークンのみ取得
        token = token.split(" ")[1]
        
        # JWT トークンをデコードして中身を取得
        decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        
        # トークン内の user_id と引数の user_id を比較
        if decoded_token["user_id"] == user_id:
            return True
        else:
            return False
    
    except Exception as e:
        # トークンが無効やデコードエラーの場合、False を返す
        return False


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
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user_id = str(ULID())
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)
    

    with get_db_cursor() as cursor:
        cursor.execute(
        "INSERT INTO users (user_id, email, name, hashed_password) VALUES (%s, %s, %s, %s)",
        (user_id, email, username, hashed_password)
    )


    return jsonify({"message": "User registered successfully"}), 201


# ログイン
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = authenticate_user(username, password)

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


# トークン認証のテスト
@app.route("/protected", methods=["GET"])
@token_required  # 認証を適用
def protected_route(current_user):
    # 認証が通ったユーザーのみアクセス可能なエンドポイント
    return jsonify({"message": f"Hello User {current_user}, you have access to this route"}), 200


# 質問生成
@app.route("/gen_question", methods=["GET"])
@token_required
def gen_question(current_user):
    try:
        # ユーザー名と頭痛ダイアリーに関する質問を生成する
        with get_db_cursor() as cursor:
            cursor.execute("SELECT name FROM users WHERE user_id = %s", (current_user,))
            user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # 質問を生成（例として頭痛に関連する簡単な質問）
        question = f"{user['name']}さん、今日の頭痛の調子はいかがでしたか？"
        # TODO: より高度な質問生成

        return jsonify({"question": question}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)