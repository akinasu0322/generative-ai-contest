from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import jwt
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from functools import wraps
from ulid import ULID


app = Flask(__name__)
app.config["SECRET_KEY"] = "Gen-ai-contest-password"
TIME_ZONE = pytz.timezone("Asia/Tokyo")
TIMEOUT_HOUR = 1


# データベース接続
def get_db_connection():
    load_dotenv()
    connection = mysql.connector.connect(
        host = os.getenv("RDS_END_POINT"),
        user = os.getenv("RDS_USER") ,
        password = os.getenv("RDS_PASS"),
        database = os.getenv("RDS_DB_NAME")
    )
    return connection


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
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, email, name, hashed_password) VALUES (%s, %s, %s, %s)",
        (user_id, email, username, hashed_password)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "User registered successfully"}), 201


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


# トークン認証デコレータ
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1]  # "Bearer <token>" の形式を想定
            print(token)
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user_id"]
        except Exception as e:
            return jsonify({"error": "Invalid token!"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


# トークン認証を行うテストAPI
@app.route("/protected", methods=["GET"])
@token_required  # 認証を適用
def protected_route(current_user):
    # 認証が通ったユーザーのみアクセス可能なエンドポイント
    return jsonify({"message": f"Hello User {current_user}, you have access to this route"}), 200



#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)