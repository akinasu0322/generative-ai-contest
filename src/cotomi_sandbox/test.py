# 必要なモジュールをインポート
import requests # HTTP通信の機能
import json # JSONデータの操作機能
from datetime import datetime # 日付に関する機能
from zoneinfo import ZoneInfo # タイムゾーンを扱う機能
from dotenv import load_dotenv # 環境変数を読み込む機能
import os # OSに関する機能
from tenacity import retry

# KEYはAPIキー.
load_dotenv()
KEY = os.getenv("COTOMI_API_KEY")
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 一般対話を行う関数. ストリーミングはオフ
# @retry()
def normal_chat(
    user_content, # ユーザプロンプト.
    system_content="あなたはAIアシスタントです。", # システムプロンプト.
    client_id="default_user", # APIの使用者を指定するID文字列.
    history_id="new", # 会話履歴ID.
    temperature=0.1, # LLMのランダム性パラメータ.
    is_oneshot=False, # 履歴を使用するかしないか.
    max_tokens=1024 # LLMのトークン数
    ):
    
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-api/v1/chat"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    headers = { "content-type": "application/json",
                "x-nec-cotomi-client-id": client_id,
                "Authorization": key }
    
    # HTTPリクエストのボディ部分.
    # プロンプトについての情報が入る.
    payload = { "userContent": user_content,
                "systemContent": system_content,
                "historyId": history_id,
                "temperature": temperature,
                "model": MODEL,
                "oneshot": is_oneshot,
                "maxTokens": max_tokens}
    
    # HTTPリクエストを送信
    # ResponseオブジェクトはHTTPレスポンスが入ってくる
    response = requests.post(url, json=payload, headers=headers)
    # Responseオブジェクトを返り値として返す
    return response


if __name__ == "__main__":
    # ストリーミング無し一般対話
    # system_content = "あなたは医者です。専門は頭痛科です。"
    # user_content = """
    # 頭が痛いです。日記の内容から、頭痛の原因が何か特定してください。原因として考えられる候補は誘発要因リストで与えられます。
    # 誘発要因リスト: まぶしい光, 騒音, 強い匂い, 熱いお湯に入浴, 人混み
    # 日記: 今日は、朝から仕事に出かけました。通勤直後とても頭が痛くなり、上司にお願いして午前で上がらせてもらいました。家に帰ると何も父親が料理をしており、さらに症状がひどくなりました。
    # """
    user_content = "関ヶ原の戦いで勝利したのは誰ですか？"
    system_content = "私はAIアシスタントです。"
    user_content = "関ヶ原の戦いで勝利したのは誰ですか？"

    res1 = normal_chat(user_content=user_content, system_content=system_content)
    print(res1.status_code)
    print(res1.text)
    print(res1.json()["answer"])
    print(res1.json()["historyId"])