import requests
import json
import os
from app.api.analyze import preprocess

# KEYはAPIキー.
KEY = os.environ.get('COTOMI_API_KEY')
# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 検索対話を行う関数. ストリーミングはオフ.
def search_chat(
    user_content, # ユーザプロンプト.
    vector_index, # インデックス名.
    system_content="あなたはAIアシスタントです", # システムプロンプト.
    client_id="DEFAULT", # クライアントID.
    history_id="new", # 会話履歴ID.
    temperature=0,  # LLMのランダム性パラメータ.
    search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
    is_oneshot=False, # 単発の会話にするかどうか.
    max_tokens=1024 # LLMトークンの最大値.
    ):
    
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-api/v1/searchchat"
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

user_prompt_perfix="""以下の会話文から頭痛の要因について30字程度でまとめ，患者にアドバイスする文章を作成してください．
## 会話文
"""
system_prompt="""あなたはAIアシスタントです"""


dummydata="""以下の会話文から頭痛の要因について30字程度で簡潔にまとめ、一文で出力してください。また、患者にアドバイスする文章を作成してください。
## 会話文    
医者「最近、食生活で変えたことや、新しい食品を足したことはありますか？」
患者「最近辛いものたくさん食べたよ」
医者「最近、辛いものをよく食べましたか？それが偏頭痛の原因かもしれません。辛い食べ物は、片頭痛の発作を引き起こすことが知られています。食生活の見直しも、偏頭痛の改善に役立つかもしれません。」
患者「わかった」
医者「最近、辛い食べ物を頻繁に食べましたか？それが偏頭痛の要因である可能性があります。食生活において、刺激の強い食品の摂取を減らすことで、偏頭痛の改善が期待できます。」
患者「うん」
医者「最近、頭痛が起こる前に、何か共通する食事のパターンはありましたか？」
患者「共通するパターンは無かったかな」
医者「偏頭痛の発作と、食事のパターンとの関連性を探ることは重要です。共通するパターンがなかった場合でも、食事日記をつけることで、偏頭痛を引き起こす可能性のある食品を特定できる可能性があります。食事日記には、食べたものと、食べた時間と偏頭痛の症状を記録してください。」
患者「りょ」"""
#ToDo 会話データを持ってこれるようにidを設定
def create_summary(chat_id):
    question, answer = preprocess(chat_id)

    #ユーザープロンプトの作成
    user_prompt=user_prompt_perfix
    for i in range(0,len(question)):
        user_prompt+=("医者: "+question[i]+"\n")
        user_prompt+=("患者: 「"+answer[i]+"」\n")

    #cotomiに投げる
    responce=search_chat(user_content=user_prompt,vector_index="headache",system_content=system_prompt,temperature=0.05)
    result=responce.json()["answer"]
    return result


# if __name__ == "__main__":
#     # ストリーミング無しの検索対話の呼び出し
#     print(search_chat("""以下の会話文から頭痛の要因について30字程度でまとめ，患者にアドバイスする文章を作成してください．
# ## 会話文    
# 医者「最近、食生活で変えたことや、新しい食品を足したことはありますか？」
# 患者「最近辛いものたくさん食べたよ」
# 医者「最近、辛いものをよく食べましたか？それが偏頭痛の原因かもしれません。辛い食べ物は、片頭痛の発作を引き起こすことが知られています。食生活の見直しも、偏頭痛の改善に役立つかもしれません。」
# 患者「わかった」
# 医者「最近、辛い食べ物を頻繁に食べましたか？それが偏頭痛の要因である可能性があります。食生活において、刺激の強い食品の摂取を減らすことで、偏頭痛の改善が期待できます。」
# 患者「うん」
# 医者「最近、頭痛が起こる前に、何か共通する食事のパターンはありましたか？」
# 患者「共通するパターンは無かったかな」
# 医者「偏頭痛の発作と、食事のパターンとの関連性を探ることは重要です。共通するパターンがなかった場合でも、食事日記をつけることで、偏頭痛を引き起こす可能性のある食品を特定できる可能性があります。食事日記には、食べたものと、食べた時間と偏頭痛の症状を記録してください。」
# 患者「りょ」""", "headache").json()["answer"])
    
# create_summary("aa")