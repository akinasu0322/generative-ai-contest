# 必要なモジュールをインポート
import requests # HTTP通信の機能
import json # JSONデータの操作機能
import os # OSに関する機能
from app.cotomi_sandbox.questions.question import questions

KEY = os.getenv("COTOMI_API_KEY")
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 一般対話を行う関数. ストリーミングはオフ
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
    results = []
    for question_dict in questions:
        system_content = question_dict["system_content"]
        user_content = question_dict["user_content"]
        res = normal_chat(system_content=system_content, user_content=user_content, temperature=0.0)
        results.append({
            "system_content" : system_content,
            "user_content" : user_content,
            "answer" : res.json()
        })

    results_path = "app/cotomi_sandbox/questions/results.json"

    # 既存のデータを読み込む
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                # JSONファイルが空だったり不正な場合
                existing_data = []
    else:
        existing_data = []

    # 新しいデータを追加する
    existing_data.extend(results)  # resultsのデータを既存のデータに追加

    # 追加後のデータを保存する
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
