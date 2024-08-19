import requests

# KEYはAPIキー.
KEY = "XXXXXXXXXXXXXX"
# GROUP_IDはグループID.
GROUP_ID = "group_xxxxxxxxxx"
# TENANT_IDはテナントID.
TENANT_ID = "T9999999"

# 新規インデックスを作成.
# インデックス名は半角アルファベット、数字、ハイフンのみで構成される必要がある
def create_index(index):
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/createIndex/"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分.
    # テナントIDを指定.
    headers = { "content-type": "application/json",
                "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key
            }
    # HTTPリクエストのボディ部分.
    # 新規作成するインデックス名を指定.
    # グループIDを指定
    payload = { "vectorIndex" : index,
                "groupId": GROUP_ID
                }
    
    # HTTPリクエストを送信.
    # ResponseオブジェクトはHTTPレスポンスが入ってくる.
    response = requests.post(url, headers=headers, json=payload)
    # Responseオブジェクトを返り値として返す.
    return response

# インデックス一覧を取得する関数.
def get_index_list():
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/listIndex/"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key,
                }
    
    # HTTPリクエストを送信
    response = requests.get(url, headers=headers)
    return response

# 指定したインデックスを削除する関数
def delete_index(index):
    # APIエンドポイントURL.
    # index: 削除したいインデックス名
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/deleteIndex?vectorIndex=" + index
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key }
    
    # HTTPリクエストを送信
    response = requests.delete(url, headers=headers)
    return response

# 指定したインデックスに登録されている文書一覧を取得する関数
def get_document_list(index):
    # APIエンドポイントのURL.
    # index: 指定するインデックス名
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/document/listDocument?vectorIndex=" + index
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key
            }
    
    # HTTPリクエストを送信
    response = requests.get(url, headers=headers)
    return response

# 指定したインデックスに登録されている文書ファイルを削除する関数
def delete_document(index, file_path):
    # APIエンドポイントURL.
    # index: 削除したいファイルが登録されているインデックス名
    # file_path: 削除したいファイルのパス
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/document/deleteDocument?vectorIndex=" + index + "&filePath=" + file_path
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key }
    # HTTPリクエストを送信
    response = requests.delete(url, headers=headers)
    return response


if __name__ == "__main__":
    import json
    # インデックスの作成
    create_index("<インデックス名>")
    # インデックスリストの表示
    print(json.dumps(get_index_list().json(), indent=2, ensure_ascii=False))
    # インデックスの削除
    delete_index("<インデックス名>")
    # 登録文書リストの表示
    print(json.dumps(get_document_list("<インデックス名>").json(), indent=2, ensure_ascii=False))
    # 登録文書の削除
    delete_document("<インデックス名>", "<ファイル名>")
    