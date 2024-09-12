################# analyse original ####################
# 必要なモジュールをインポート
import requests # HTTP通信の機能
import json # JSONデータの操作機能
import os
from app.db.db_tools import get_db_cursor

#ToDo APIキーの取得
if os.environ.get('COTOMI_API_KEY')==None:
    print("Please set environment value COTOMI_API_KEY=hogehoge")
    exit(1)
# KEYはAPIキー. 絶対公開しない!!!!!!!!!!!!
KEY=os.environ["COTOMI_API_KEY"]
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 一般対話を行う関数. ストリーミングはオフ
def normal_chat(
    user_content, # ユーザプロンプト.
    system_content="あなたはAIアシスタントです", # システムプロンプト. #ToDo ここをかえてもいい
    client_id="default_user", # APIの使用者を指定するID文字列.
    history_id="new", # 会話履歴ID.    #ToDo 会話を続けたい場合はここを前のidにする
    temperature=0, # LLMのランダム性パラメータ.
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


system_prompt="""あなたはAIアシスタントです．以下の会話文から以下の情報をすべてCSV形式で出力してください．会話文から読み取れる内容のみ出力してください．値は「あり」，「なし」，「不明」のいずれかにしてください．
強い光
不快な匂い
入浴
天候変化
気温変化
人混み
乳製品
アルコール
魚の燻製
ナッツ
チョコレート
中華料理
月経
ピルの服用
体偏屈や体の姿勢
重いものを持つ
激しい運動
長時間の運転
旅行
睡眠
歯痛
他の頭痛
頸部痛
高血圧
ショック
ストレス
頭痛の強さ
薬を飲んだか
薬の効き
使っている薬

## 例
強い光, あり
不快な匂い, 不明
入浴, あり
天候変化, あり
気温変化, 不明
人混み, あり
乳製品, あり
アルコール, なし
魚の燻製, 不明
ナッツ, あり
チョコレート, 不明
中華料理, 不明
月経, あり
ピルの服用, なし
体偏屈や体の姿勢, あり
重いものを持つ, あり
激しい運動, 不明
長時間の運転, なし
旅行, あり
睡眠, あり
歯痛, 不明
他の頭痛, 不明
頸部痛, なし
高血圧, あり
ショック, 不明
ストレス, なし
頭痛の強さ, なし
薬を飲んだか, なし
薬の効き, あり
使っている薬, なし
"""

def preprocess(chat_id):
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT question, answer
            FROM questions
            WHERE chat_id = %s
            ORDER BY index_in_chat ASC
            """,
            (chat_id,)
        )
        result = cursor.fetchall()
    question=[row["question"] for row in result]
    answer=[row["answer"] for row in result]
    return question, answer

# ステップ 1: 日本語キーと英語キーの対応辞書
transform_dict = {
    '強い光': 'strong_light',
    '不快な匂い': 'unpleasant_odor',
    '入浴': 'took_bath',
    '天候変化': 'weather_change',
    '気温変化': 'temperture_change',
    '人混み': 'crowds',
    '乳製品': 'dairy_products',
    'アルコール': 'alcohol',
    '魚の燻製': 'smoked_fish',
    'ナッツ': 'nuts',
    'チョコレート': 'chocolate',
    '中華料理': 'chinese_food',
    '月経': 'menstruation',
    'ピルの服用': 'pill_taken',
    '体偏屈や体の姿勢': 'body_posture',
    '重いものを持つ': 'carried_heavy_object',
    '激しい運動': 'intense_exercise',
    '長時間の運転': 'long_driving',
    '旅行': 'travel',
    '睡眠': 'sleep',
    '歯痛': 'toothache',
    '他の頭痛': 'headache_intensity',
    '頸部痛': 'neck_pain',
    '高血圧': 'hypertension',
    'ショック': 'shock',
    'ストレス': 'stress',
    '頭痛の強さ': 'headache_intensity',
    '薬を飲んだか': 'medicine_taken',
    '薬の効き': 'medicine_effect',
    '使っている薬': 'medicine_name'
}

# ステップ 2: 日本語のキーを英語のキーに変換する関数
def translate_keys(ja_dict, transform_dict):
    en_dict = {}
    for ja_key, value in ja_dict.items():
        # 日本語キーが変換辞書に存在すれば、英語キーに変換
        if ja_key in transform_dict:
            en_key = transform_dict[ja_key]
            en_dict[en_key] = value
    return en_dict

#ToDo 会話を取得できるように引数を変更
def analyzer(chat_id):
    question, answer = preprocess(chat_id)
    
    #ユーザープロンプトの作成
    print(f"q_len={len(question)}, a_len={len(answer)}")
    user_prompt=""
    for i in range(0,len(question)):
        user_prompt+=("医者: "+question[i]+"\n")
        user_prompt+=("患者: 「"+answer[i]+"」\n")

    #Cotomiに投げる
    responce = normal_chat(user_prompt, system_content=system_prompt, temperature=0, is_oneshot=True)
    #ToDo? ここにエラーチェック挟むべきかも

    #ここからデータの整形
    result_dict=dict()
    lines=responce.json()["answer"].splitlines()
    for line in lines:
        keyval=line.split(',')
        if len(keyval)>=2:
            if "あり" in keyval[1]:
                result_dict[keyval[0]]=True
            elif "なし" in keyval[1]:
                result_dict[keyval[0]]=False
            else:
                result_dict[keyval[0]]=None
    #result_dictにkey-value形式で抽出結果が入っている
    print(result_dict)
    en_dict = translate_keys(result_dict, transform_dict)
    return en_dict

# analyzer("aa")

# if __name__ == "__main__":
#     prev_hitoryid="new"
#     log_cotomi=[]
#     log_patient=[]
#     res = normal_chat(text,history_id=prev_hitoryid) #res1に結果が返ってくる
#     print(res)
#     print(res.json()["answer"])
#     result_dict=dict()
#     lines=res.json()["answer"].splitlines()
#     for line in lines:
#         keyval=line.split(',')
#         print(keyval)
#         if len(keyval)>=2:
#             if "あり" in keyval[1]:
#                 result_dict[keyval[0]]=True
#             elif "なし" in keyval[1]:
#                 result_dict[keyval[0]]=False
#             else:
#                 result_dict[keyval[0]]=None
#     print(result_dict)