# 必要なモジュールをインポート
import requests # HTTP通信の機能
import json # JSONデータの操作機能
from datetime import datetime # 日付に関する機能
from zoneinfo import ZoneInfo # タイムゾーンを扱う機能
from dotenv import load_dotenv # 環境変数を読み込む機能
import os # OSに関する機能

# KEYはAPIキー.
load_dotenv()
KEY = os.getenv("COTOMI_API_KEY")
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"





####################################################################################################
# 一般対話を行う関数. ストリーミングはオフ
def normal_chat(
    user_content, # ユーザプロンプト.
    system_content="あなたはAIアシスタントです。", # システムプロンプト.
    client_id="default_user", # APIの使用者を指定するID文字列.
    history_id="new", # 会話履歴ID.
    temperature=1, # LLMのランダム性パラメータ.
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

# 一般対話を行うジェネレータ関数. ストリーミングはオン.
def normal_chat_streaming(
    user_content, # ユーザプロンプト.
    system_content="あなたはAIアシスタントです。", # システムプロンプト.
    client_id="default_user", # APIの使用者を指定するID文字列.
    history_id="new", # 会話履歴ID.
    temperature=1, # LLMのランダム性パラメータ.
    is_oneshot=False, # 履歴を使用するかしないか.
    max_tokens=1024, # LLMのトークン数
    stream_num=10 # 何文字単位でレスポンスを返却するか
    ):
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-api/v1/chat"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのボディ部分.
    # プロンプトについての情報が入る.
    payload = { "userContent": user_content,
                "systemContent": system_content,
                "historyId": history_id,
                "temperature": temperature,
                "model": MODEL,
                "oneshot": is_oneshot,
                "stream": True,
                "streamNum": stream_num,
                "maxTokens": max_tokens}
    
    # HTTPリクエストのヘッダ部分
    headers = { "content-type": "application/json",
                "x-nec-cotomi-client-id": client_id,
                "Authorization": key }
    
    # ストリーム形式でPOSTリクエスト送信、レスポンスを逐次受信.
    with requests.post(url, json=payload, headers=headers, stream=True) as response:
        # HTTPのエラー.
        if not response.status_code == 200 :
            data = None
            try :
                data = response.json() # エラーメッセージ.
            except Exception as e:
                print(e)
            finally:
                now = datetime.now(ZoneInfo("Asia/Tokyo"))
                # エラー内容を標準出力.
                print("ERROR,DATE,{},httpStatus,{},errorMsg,{}".format(now.time().isoformat(timespec="seconds"), str(response.status_code), data))
                raise TypeError()
        try:
            # サーバー送信イベント (SSE)のストリーミング. MDNのドキュメント参照のこと(https://developer.mozilla.org/ja/docs/Web/API/Server-sent_events/Using_server-sent_events).
            for chunk in response.iter_lines(decode_unicode=True): # 分割されたレスポンスを1つずつ取ってくる.
                if chunk is None: # 空のチャンクはスキップ.
                    continue
                if chunk.startswith("event:done") : # ストリームの終端.
                    break
                if not chunk.startswith("data:") : # イベントメッセージを読み捨てる(表示させたい場合はこの中で処理を記述してください).
                    continue
                
                data = json.loads(chunk[6:]) # "data: "を切り捨て.
                if "answer" in data:
                    yield data["answer"] # 細切れのレスポンスを返す.
                if "error" in data:
                    yield data["error"] # 途中に発生したエラーメッセージを返す.
        except Exception as e:
            # 予期せぬエラーキャッチ
            print(e)
            now = datetime.now(ZoneInfo("Asia/Tokyo"))
            print("ERROR,DATE,{},httpStatus,{},line,{}".format(now.time().isoformat(timespec="seconds"), str(response.status_code), chunk))

if __name__ == "__main__":
    # ストリーミング無し一般対話
    res1 = normal_chat("<プロンプト>")
    print(res1.status_code)
    print(res1.text)
    print(res1.json()["answer"])
    print(res1.json()["historyId"])
    
    #ストリーミングあり一般対話
    for chunk in normal_chat_streaming("<プロンプト>"):
        print(chunk, end="")