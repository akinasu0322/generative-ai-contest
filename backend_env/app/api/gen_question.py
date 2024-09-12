# 必要なモジュールをインポート
import requests # HTTP通信の機能
import json # JSONデータの操作機能
import os
import random

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
    system_content="""あなたは優しい医者です。""", # システムプロンプト. #ToDo ここをかえてもいい
    client_id="default_user", # APIの使用者を指定するID文字列.
    history_id="new", # 会話履歴ID.    #ToDo 会話を続けたい場合はここを前のidにする
    temperature=0.05, # LLMのランダム性パラメータ.
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

#factorを列挙
factor_arr=["強い光","不快な匂い","入浴","天候変化","気温変化","人混み","乳製品","アルコール","魚の燻製","ナッツ","チョコレート","中華料理","月経","ピルの服用","体偏屈や体の姿勢","重いものを持つ","激しい運動 ","長時間の運転 ","旅行 ","睡眠 ","歯痛 ","他の頭痛 ","頸部痛 ","高血圧 ","ショック ","ストレス ","頭痛の強さ ","薬を飲んだか ","薬の効き ","使っている薬"]

first_prefix="""偏頭痛患者に偏頭痛の要因の有無を訊く30字程度の質問を生成してください．要因として考えられるものは以下のとおりです．
""" #プロンプト
next_prefix="""

続けて，以下の要因についても30文字程度で質問してください．
要因:
"""
answer_prefix="""返答:\n"""


def get_true_indices(list_data):
    """
    リスト内のTrueの要素のインデックスをリストで返す

    Args:
        list_data (list): 対象のリスト

    Returns:
        list: Trueの要素のインデックスのリスト
    """

    return [i for i, x in enumerate(list_data) if x]

#新しい質問を生成する 生成して質問文とhistory_idをreturn
#factor_tableは適宜sessionから取れる各要因についてすでに質問した=Falseかしてない=Trueか
def function_for_get_question(factor_unused_list,history_id="new",prompt_prefix=first_prefix):
    prompt=prompt_prefix
    #factorを選んで追加
    for i in range(0,3):
        rand=random.choice(get_true_indices(factor_unused_list))
        fac=factor_arr[rand]
        prompt+=("\n"+fac)

        factor_unused_list[rand]=False #session内のtableを更新する
    

    print("prompt:\n",prompt)
    response = normal_chat(prompt,history_id=history_id)
    print(response)
    history_id=response.json()["historyId"] #session内のhistoryidを更新する
    return response.json()["answer"], history_id

    pass
#回答を受け取る 
def function_for_post_answer(answer):
    #この処理をsessionのprompt_prefixを変更する処理に変える
    return answer_prefix+answer+next_prefix


# if __name__ == "__main__":
#     prev_hitoryid="new"
    
#     prompt=first_prefix
#     for i in range(0,5):
#         #factorを選んで追加
#         for j in range(0,3):
#             rand=random.randint(0,len(factor)-1)
#             fac=factor[rand]
#             prompt+=("\n"+fac)
#             factor.remove(fac)
#         log_prompt.append(prompt)
#         print("prompt:\n",prompt)
#         res = normal_chat(prompt,history_id=prev_hitoryid) #res1に結果が返ってくる
#         print(res)
#         print(res.json()["answer"])
#         prev_hitoryid=res.json()["historyId"]
#         log_cotomi.append(res.json()["answer"])
#         # print(res.json()["historyId"])
#         patient_answer=input()
#         prompt=answer+patient_answer+next_prefix
#         log_patient.append(patient_answer)
#     print("-----")
#     for i in range(0,5):
#         print("医者: "+log_cotomi[i])
#         print("患者: 「"+log_patient[i]+"」")
#     print("-----")
#     print(log_cotomi)
#     print(log_patient)
#     print(log_prompt)

factor_table=[True for i in range(0,len(factor_arr))]
if __name__=="__main__":
    question,id=function_for_get_question(factor_table,"new")
    print(question)
    prefix=function_for_post_answer(input(),"")
    
    question,id=function_for_get_question(factor_table,id,prefix)
    print(question)
    function_for_post_answer(input(),"")
    
    question,id=function_for_get_question(factor_table,id,prefix)
    print(question)
    function_for_post_answer(input(),"")
    
    question,id=function_for_get_question(factor_table,id,prefix)
    print(question)
    function_for_post_answer(input(),"")
    
    pass