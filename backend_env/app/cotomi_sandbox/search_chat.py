import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo


# KEYはAPIキー.
KEY = "XXXXXXXXXXXXXX"
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 検索対話を行う関数. ストリーミングはオフ.
def search_chat(
    user_content, # ユーザプロンプト.
    vector_index, # インデックス名.
    system_content="あなたはAIアシスタントです", # システムプロンプト.
    client_id="DEFAULT", # クライアントID.
    history_id="new", # 会話履歴ID.
    temperature=1,  # LLMのランダム性パラメータ.
    search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
    is_oneshot=False, # 単発の会話にするかどうか.
    max_tokens=1024 # LLMトークンの最大値.
    ):
    
    # APIエンドポイントのURL.
    url = "https://api-dev.cotomi-test.nec-cloud.com/cotomi-api/v1/searchchat"
    # 認証パラメータ.
    key = "Bearer " + KEY
    
    # リクエストボディのパラメータ指定.
    payload = { "userContent": user_content,
                "systemContent": system_content,
                "vectorIndex": vector_index,
                "historyId": history_id,
                "temperature": temperature,
                "model": MODEL,
                "searchOption": search_option,
                "onshot": is_oneshot,
                "maxTokens": max_tokens}
    
    # リクエストヘッダのパラメータ指定.
    headers = { "content-type": "application/json",
                "x-nec-cotomi-client-id": client_id,
                "Authorization": key }
    
    # POSTリクエスト送信、レスポンス受信.
    response = requests.post(url, json=payload, headers=headers)
    return response

# 検索対話を行うジェネレータ関数. ストリーミングはオン.
def search_chat_streaming(
    user_content, # ユーザプロンプト.
    vector_index, # インデックス名.
    system_content="あなたはAIアシスタントです", # システムプロンプト.
    client_id="DEFAULT", # クライアントID.
    history_id="new", # 会話履歴ID.
    temperature=1,  # LLMのランダム性パラメータ.
    search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
    is_oneshot=False, # 単発の会話にするかどうか.
    stream_num=10, # ストリーミング時に何文字単位で返すか.
    max_tokens=1024 # LLMトークンの最大値.
    ):
    
    # APIエンドポイントのURL.
    url = "https://api-dev.cotomi-test.nec-cloud.com/cotomi-api/v1/searchchat"
    # 認証パラメータ.
    key = "Bearer " + KEY
    
    # リクエストボディのパラメータ指定.
    payload = { "userContent": user_content,
                "systemContent": system_content,
                "vectorIndex": vector_index,
                "historyId": history_id,
                "temperature": temperature,
                "model": MODEL,
                "searchOption": search_option,
                "onshot": is_oneshot,
                "stream": True,
                "streamNum": stream_num,
                "maxTokens": max_tokens}
    
    # リクエストヘッダのパラメータ指定.
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
            for chunk in response.iter_lines(decode_unicode=True): # 分割されたレスポンスを1つずつ処理.
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
    # ストリーミング無しの検索対話の呼び出し
    print(search_chat("<prompt>", "<index name>").text)
    
    # ストリーミングありの検索対話の呼び出し
    for talk in search_chat_streaming("<prompt>", "<index name>"):
        print(talk, end="")