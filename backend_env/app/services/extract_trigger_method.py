"""
誘発因子抽出メソッド
・概要
    ・質問に対する回答から、誘発因子を抽出する
・入力
    ・回答文(str)
    ・特定したい誘発因子(list)
・出力
    ・誘発因子(dict)
        ・誘発因子名(str): 誘発因子の値(str)
"""

def method(answer:str, triggers:list[str]) -> dict[str, str]:
    result = {}
    for trigger in triggers:
        if trigger in answer:
            result[trigger] = answer
    return result


