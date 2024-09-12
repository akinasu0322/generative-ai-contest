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
    ###### <COMPONENT : register_user> ######
    ####################################
    # 新規ユーザー登録
    def component_register_user(
            self, 
            email="hello@gmail.com",
            user_name="testuser",
            password="testpassword",
            age=30,
            sex="male",
            prefecture="Tokyo",
            medicine_name="TestMed",
            status_code=201 # 201 Createdを期待
        ):
        response = requests.post(
            url = f'{END_POINT}/register_user',
            headers = {'content_type': 'application/json'},
            json = {
                'email': email,
                'user_name': user_name,
                'password': password,
                'age': age,
                'sex': sex,
                'prefecture': prefecture,
                'medicine_name': medicine_name
            },
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    ####################################
    ###### <COMPONENT : register_doctor> ######
    ####################################
    # 新規医者登録
    def component_register_doctor(
            self, 
            email="doctor@gmail.com",
            user_name="doctoruser",
            password="docpassword",
            age=40,
            sex="female",
            hospital_id="1",
            status_code=201 # 201 Createdを期待
        ):
        response = requests.post(
            url = f'{END_POINT}/register_doctor',
            headers = {'content_type': 'application/json'},
            json = {
                'email': email,
                'user_name': user_name,
                'password': password,
                'age': age,
                'sex': sex,
                'hospital_id': hospital_id
            },
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()
    

    ####################################
    ###### <COMPONENT : register_hospital> ######
    ####################################
    # 新規病院登録
    def component_register_hospital(
            self, 
            hospital_name="Test Hospital",
            hospital_code="HOSP123",
            password="hospitalpass",
            status_code=201 # 201 Createdを期待
        ):
        response = requests.post(
            url = f'{END_POINT}/register_hospital',
            headers = {'content_type': 'application/json'},
            json = {
                'hospital_name': hospital_name,
                'hospital_code': hospital_code,
                'password': password
            },
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()


    ####################################
    ###### <COMPONENT : login> ######
    ####################################
    # ログイン
    def component_login(
            self,
            email="hello@gmail.com",
            password="testpassword",
            role="user",
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/login',
            headers = {'content_type': 'application/json'},
            json = {'email': email, 'password': password, 'role': role}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    #########################################
    ###### <COMPONENT : register_in_charge_user> ######
    #########################################
    # 担当患者の追加
    def component_register_in_charge_user(
            self,
            jwt_token="token",
            user_id="user123",
            status_code=200 # 200 OKを期待
        ):
        response = requests.post(
            url = f'{END_POINT}/register_in_charge_user',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'user_id': user_id}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    ########################################
    ###### <COMPONENT : get_in_charge_users_info> ######
    ########################################
    # 担当患者の情報取得
    def component_get_in_charge_users_info(
            self,
            jwt_token="token",
            status_code=200
        ):
        response = requests.get(
            url = f'{END_POINT}/get_in_charge_users_info',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    #######################################
    ###### <COMPONENT : get_user_info> ######
    #######################################
    # ユーザー情報取得
    def component_get_user_info(
            self,
            jwt_token="token",
            user_id="user",
            recent_k=3,
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/get_user_info',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'user_id': user_id, 'recent_k': recent_k}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()
    

    ####################################
    ###### <COMPONENT : start_chat> ######
    ####################################
    # チャットの開始
    def component_start_chat(
            self,
            jwt_token="token",
            status_code=201,
            call_time='0000-00-00-00'
        ):
        response = requests.post(
            url = f'{END_POINT}/start_chat',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'call_time': call_time}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()


    ####################################
    ###### <COMPONENT : gen_question> ######
    ####################################
    # 質問の生成
    def component_gen_question(
            self,
            jwt_token="token",
            chat_id="chat_id",
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/gen_question',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'chat_id': chat_id}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()


    ####################################
    ###### <COMPONENT : post_answer> ######
    ####################################
    # 回答の送信
    def component_post_answer(
            self,
            jwt_token="token",
            chat_id="chat_id",
            question_id="question_id",
            answer="Yes",
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/post_answer',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {
                'chat_id': chat_id,
                'question_id': question_id,
                'answer': answer
            }
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()


    ####################################
    ###### <COMPONENT : gen_summary> ######
    ####################################
    # サマリーの生成
    def component_gen_summary(
            self,
            jwt_token="token",
            chat_id="chat_id",
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/gen_summary',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'chat_id': chat_id}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()
    

    ####################################
    ###### <COMPONENT : post_questionnaire_result> ######
    ####################################
    # アンケート結果の記録
    def component_post_questionnaire_result(
            self,
            jwt_token="token",
            questionnaire_title="mibs4",
            answer=[3, 1, 0, 2],
            status_code=201
        ):
        response = requests.post(
            url = f'{END_POINT}/post_questionnaire_result',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {
                'questionnaire_title': questionnaire_title,
                'answer': answer
            }
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()
    

    #############################################
    ###### <COMPONENT : get_questionnaire_result> ######
    #############################################
    # アンケート結果の取得
    def component_get_questionnaire_result(
            self,
            jwt_token="token",
            user_id="user123",
            recent_k=1,
            questionnaire_title="mibs4",
            status_code=200
        ):
        response = requests.post(
            url = f'{END_POINT}/get_questionnaire_result',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'user_id': user_id, 'recent_k': recent_k, 'questionnaire_title': questionnaire_title}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    ######################
    ####### <TEST> #######
    ######################
    # チャットフローのテスト
    def test_chat_flow(self):
        # ユーザー登録、ログイン、チャット開始、質問生成、回答送信、サマリー生成の流れをテスト

        # 1. ユーザー登録
        self.component_register_user(
            email="testuser@gmail.com",
            user_name="TestUser",
            password="password123",
            age=30,
            sex="male",
            prefecture="Tokyo",
            medicine_name="TestMed"
        )

        # 2. ログイン
        login_response = self.component_login(
            email="testuser@gmail.com",
            password="password123",
            role="user"
        )
        jwt_token = login_response['jwt_token']
        user_id = login_response["user_id"]

        # 3. チャット開始
        chat_response = self.component_start_chat(jwt_token=jwt_token)
        chat_id = chat_response["chat_id"]

        # 4. 質問生成
        question_response = self.component_gen_question(
            jwt_token=jwt_token,
            chat_id=chat_id
        )
        question_id = question_response["question_id"]

        # 5. 回答送信
        self.component_post_answer(
            jwt_token=jwt_token,
            chat_id=chat_id,
            question_id=question_id,
            answer="My head hurts."
        )

        # 6. サマリー生成
        self.component_gen_summary(
            jwt_token=jwt_token,
            chat_id=chat_id
        )

        # 7. アンケート結果の記録
        self.component_post_questionnaire_result(
            jwt_token=jwt_token,
            questionnaire_title="mibs4",
            answer=[3, 1, 0, 2]
        )

        # 8. ユーザー情報の取得
        response = self.component_get_user_info(
            jwt_token=jwt_token,
            user_id=user_id,
            recent_k=1
        )
        print(response)

        
    # ユーザー登録、ログイン、アンケート取得のテスト
    def test_register_and_get_questionnaire(self):
        ### 患者さんパート
        # ユーザー登録
        self.component_register_user(
            email="testuser2@gmail.com",
            user_name="TestDoctor2",
            password="password123",
            age=12,
            sex="female",
            prefecture="Tokyo",
        )

        # ログイン
        login_response = self.component_login(
            email="testuser2@gmail.com",
            password="password123",
            role="user"
        )
        jwt_token = login_response['jwt_token']
        user_id = login_response['user_id']

        # mibs4への回答
        self.component_post_questionnaire_result(
            jwt_token = jwt_token,
            questionnaire_title="mibs4",
            answer=[1,0,1,2]
        )


        ### お医者さんパート
        # 病院の登録
        response = self.component_register_hospital(
            hospital_name="Test clinic",
            hospital_code="1234567",
            password="test_clinic_password123",
        )
        hospital_id = response["hospital_id"]

        # ユーザー登録
        self.component_register_doctor(
            email="testdoctor1@gmail.com",
            user_name="TestDoctor1",
            password="password123",
            age=56,
            sex="female",
            hospital_id=hospital_id
        )

        # ログイン
        login_response = self.component_login(
            email="testdoctor1@gmail.com",
            password="password123",
            role="doctor"
        )
        jwt_token = login_response['jwt_token']

        # 担当患者の登録
        self.component_register_in_charge_user(
            jwt_token=jwt_token,
            user_id=user_id # 患者さんのuser_id
        )

        # アンケート結果取得
        response_result = self.component_get_questionnaire_result(
            jwt_token=jwt_token,
            user_id=user_id,
            recent_k=1,
            questionnaire_title="mibs4"
        )
        print(response_result)


if __name__ == '__main__':
    print("Test Start")
    unittest.main()

