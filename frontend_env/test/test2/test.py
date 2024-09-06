import unittest
import requests
import json

# サーバー情報
SERVER_IP = "13.210.90.34"
PORT = 5000
END_POINT = f"http://{SERVER_IP}:{str(PORT)}"

class FlaskTestCase(unittest.TestCase):
    # テスト前の初期化
    def setUp(self):
        pass

    ####################################
    ###### <COMPONENT : register> ######
    ####################################
    # 新規ユーザー登録
    def component_register(
            self, 
            username="testuser",
            password="testpassword",
            email="hello@gmail.com"
        ):
        response = requests.post(
            url = f'{END_POINT}/register',
            headers = {'content_type': 'application/json'},
            json = {'username': username, 'password': password, 'email': email},
        )
        self.assertEqual(response.status_code, 201) # 201 Createdを期待
        return response.json()


    # # 重複ユーザー登録
    # def component_register_duplicate(
    #         self,
    #         username="testuser",):
    #     response = requests.post(
    #         url = f'{END_POINT}/register',
    #         headers = {'content_type': 'application/json'},
    #         json = {'username': 'testuser2', 'password': 'testpassword2', 'email': 'hello@gmail.com'},
    #     )
    #     self.assertEqual(response.status_code, 409) # 409 Conflictエラーを期待

    #################################
    ###### <COMPONENT : login> ######
    #################################
    # ログイン
    def component_login(
            self,
            username="testuser",
            password="testpassword"
        ):
        response = requests.post(
            url = f'{END_POINT}/login',
            headers = {'content_type': 'application/json'},
            json = {'username': username, 'password': password}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    # # ログイン失敗（パスワードが異なる）
    # def component_login_fail(self):
    #     response = requests.post(
    #         url = f'{END_POINT}/login',
    #         headers = {'content_type': 'application/json'},
    #         json = {'username': 'test', 'password': 'wrongpassword'}
    #     )
    #     self.assertEqual(response.status_code, 401) # 401 Unauthorizedを期待

    # # ログイン失敗（ユーザーが存在しない）
    # def component_login_fail2(self):
    #     response = requests.post(
    #         url = f'{END_POINT}/login',
    #         headers = {'content_type': 'application/json'},
    #         json = {'username': 'wronguser', 'password': 'wrongpassword'}
    #     )
    #     self.assertEqual(response.status_code, 401) # 401 Unauthorizedを期待


    #############################################
    ###### <COMPONENT : gen_next_question> ######
    #############################################
    # 最初の質問を生成
    def component_gen_next_question(
            self,
            jwt_token = "token",
            chat_id = None
        ):
        response = requests.post(
            url = f'{END_POINT}/gen_next_question',
            headers = {'content_type': 'application/json', 'jwt_token': jwt_token, 'chat_id': chat_id},
            json = {'anwer': ''},
        )
        self.assertEqual(response.status_code, 200) # 200 OKを期待 
        return response.json() 

    # # 2〜n-i番目の質問を生成
    # def component_gen_next_question_middle(self):
    #     response = requests.post(
    #         url = f'{END_POINT}/login',
    #         json = {'username': 'user', 'password': 'password'},
    #         headers = {'content_type': 'application/json'}
    #     )
    #     self.assertEqual(response.status_code, 401)

    # # 最後の質問を生成
    # def component_gen_next_question_last(self):
    #     response = requests.post(
    #         url = f'{END_POINT}/login',
    #         json = {'username': 'user', 'password': 'password'},
    #         headers = {'content_type': 'application/json'}
    #     )
    #     self.assertEqual(response.status_code, 401)

    # # 質問生成失敗（ログインしていない）
    # def component_gen_next_question_fail(self):
    #     response = requests.post(
    #         url = f'{END_POINT}/login',
    #         json = {'username': 'user', 'password': 'password'},
    #         headers = {'content_type': 'application/json', 'jwt_token': 'wrong'}
    #     )
    #     self.assertEqual(response.status_code, 401)
    
    ######################################
    ####### <COMPONENT : get_info> #######
    ######################################
    # ユーザー情報取得
    def component_get_user_info(
            self,
            jwt_token="token",
            user_id="user",
            start_span="2024-05-22",
            end_span="2024-06-12"
        ):
        response = requests.get(
            url = f'{END_POINT}/get_user_info',
            headers = {'content_type': 'application/json', 'jwt_token': jwt_token},
            json = {'user_id': user_id, 'start_span': start_span, 'end_span': end_span}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    # 医者情報取得
    def component_get_doctor_info(
            self,
            doctor_id="doctor",
            jwt_token="token",
        ):
        response = requests.get(
            url = f'{END_POINT}/get_doctor_info',
            headers = {'content_type': 'application/json', 'jwt_token': jwt_token},
            json = {'doctor_id': doctor_id}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()


    # 病院情報取得
    def component_get_hospital_info(
            self,
            jwt_token="token",
            hospital_id = "hospital_id",):
        response = requests.get(
            url = f'{END_POINT}/get_hospital_info',
            headers = {'content_type': 'application/json', 'jwt_token': jwt_token},
            json = {'hospital_id': hospital_id}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()



    #############################################
    ####### <COMPONENT : protected_route> #######
    #############################################
    def component_protected_route(
            self, 
            jwt_token="token"
        ):
        response = requests.get(
            url = f'{END_POINT}/protected',
            headers = {'content_type': 'application/json', 'Authorization': jwt_token},
            json = {'key': 'value'}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()


    ######################
    ####### <TEST> #######
    ######################
    def test_register_flow1(self):
        response = self.component_register(username="testuser", password="testpassword", email="hello@gmail.com")
        response = self.component_login(username="testuser", password="testpassword")
        jwt_token = response['jwt_token']
        response = self.component_gen_next_question(jwt_token=jwt_token, chat_id=None)
        tmp_chat_id = response['chat_id']
        response = self.component_gen_next_question(jwt_token=jwt_token, chat_id=tmp_chat_id)
        tmp_chat_id = response['chat_id']
        response = self.component_gen_next_question(jwt_token=jwt_token, chat_id=tmp_chat_id)


    def test_token_required(self):
        response = self.component_register(username="testuser2", password="testpassword2", email="hello2@gmail.com")
        response = self.component_login(username="testuser2", password="testpassword2")
        jwt_token = response['jwt_token']
        print("----------------")
        print(jwt_token)
        print(type(jwt_token))
        print("----------------")
        response = self.component_protected_route(jwt_token=f"Bearer {jwt_token}")



    def test_login_fail(self):
        response = self.component_register(username="testuser3", password="testpassword3", email="hello3@gmail.com")
        response = self.component_login(username="testuser3", password="testpassword1")


    # def test_flow(self):
    #     self.component_register()
    #     self.component_login()
    #     self.component_gen_next_question()
    #     self.component_gen_next_question()
    #     self.component_gen_next_question()


if __name__ == '__main__':
    print("Test Start")
    unittest.main()
