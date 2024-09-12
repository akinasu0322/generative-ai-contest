import unittest
import requests
import json
from datetime import datetime, timedelta


# サーバー情報
SERVER_IP = "13.210.90.34"
PORT = 5000
END_POINT = f"http://{SERVER_IP}:{str(PORT)}"

class FlaskTestCase(unittest.TestCase):
    # テスト前の初期化
    def setUp(self):
        self.session = requests.Session()

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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
            email="hello@gmail.com",
            status_code=200 # 200 OKを期待
        ):
        response = self.session.post(
            url = f'{END_POINT}/register_in_charge_user',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {"email": email}
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
        response = self.session.get(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
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
        response = self.session.post(
            url = f'{END_POINT}/get_questionnaire_result',
            headers = {'content_type': 'application/json', 'Authorization': f'Bearer {jwt_token}'},
            json = {'user_id': user_id, 'recent_k': recent_k, 'questionnaire_title': questionnaire_title}
        )
        self.assertEqual(response.status_code, status_code)
        return response.json()

    ######################
    ####### <TEST> #######
    ######################
    def test_chat_flow_with_multiple_days_and_doctor(self):
        start_date = datetime(2024, 8, 7, 0, 0)  # 2024-08-07-00

        # ユーザー登録
        self.component_register_user(
            email="testuser@gmail.com",
            user_name="TestUser",
            password="password123",
            age=30,
            sex="male",
            prefecture="Tokyo",
            medicine_name="TestMed"
        )

        # ログイン
        login_response = self.component_login(
            email="testuser@gmail.com",
            password="password123",
            role="user"
        )
        jwt_token_user = login_response['jwt_token']
        user_id = login_response['user_id']

        record_days = [0,1,3,5,6,8,12,14,17,30]
        # record_days = [1,4,10]
        for i in record_days:
            current_time = start_date + timedelta(days=i)
            call_time_str = current_time.strftime('%Y-%m-%d-%H')

            # チャット開始
            chat_response = self.component_start_chat(jwt_token=jwt_token_user, call_time=call_time_str)
            chat_id = chat_response["chat_id"]

            # 5回の質問生成と回答送信
            for _ in range(5):
                question_response = self.component_gen_question(jwt_token=jwt_token_user, chat_id=chat_id)
                question_id = question_response["question_id"]

                # 回答送信
                self.component_post_answer(
                    jwt_token=jwt_token_user,
                    chat_id=chat_id,
                    question_id=question_id,
                    answer="My head hurts."
                )

            # サマリー生成
            self.component_gen_summary(jwt_token=jwt_token_user, chat_id=chat_id)

        # アンケート結果の記録 (mibs4)
        self.component_post_questionnaire_result(
            jwt_token=jwt_token_user,
            questionnaire_title="mibs4",
            answer=[3, 1, 0, 2]
        )

        # アンケート結果の記録 (hit6)
        self.component_post_questionnaire_result(
            jwt_token=jwt_token_user,
            questionnaire_title="hit6",
            answer=[4, 3, 2, 5, 1, 0]
        )

        # ユーザー情報の取得
        response = self.component_get_user_info(
            jwt_token=jwt_token_user,
            user_id=user_id,
            recent_k=3
        )
        print("----------- get user info from user ----------")
        print(response)
        print("----------------------------------------------")

        ### 医者側の操作
        # 病院の登録
        hospital_response = self.component_register_hospital(
            hospital_name="Test Hospital",
            hospital_code="HOSP123",
            password="hospitalpass"
        )
        hospital_id = hospital_response['hospital_id']

        # 医者の登録
        self.component_register_doctor(
            email="doctor@gmail.com",
            user_name="DoctorUser",
            password="doctorpass",
            age=40,
            sex="female",
            hospital_id=hospital_id
        )

        # 医者のログイン
        login_response_doctor = self.component_login(
            email="doctor@gmail.com",
            password="doctorpass",
            role="doctor"
        )
        jwt_token_doctor = login_response_doctor['jwt_token']

        # 担当患者の追加
        self.component_register_in_charge_user(
            jwt_token=jwt_token_doctor,
            user_id=user_id
        )

        # 担当患者の簡易情報取得
        response = self.component_get_in_charge_users_info(
            jwt_token=jwt_token_doctor
        )
        print("--------------- get in charge users info from doctor ---------")
        print(response)
        print("--------------------------------------------------------------")

        # 医者がユーザーの情報を取得
        response = self.component_get_user_info(
            jwt_token=jwt_token_doctor,
            user_id=user_id,
            recent_k=3
        )
        print("--------------- get user info from doctor ---------")
        print(response)
        print("---------------------------------------------------")

        # 医者がhit6のアンケート結果を取得
        self.component_get_questionnaire_result(
            jwt_token=jwt_token_doctor,
            user_id=user_id,
            recent_k=1,
            questionnaire_title="hit6"
        )

        # 医者がmibs4のアンケート結果を取得
        self.component_get_questionnaire_result(
            jwt_token=jwt_token_doctor,
            user_id=user_id,
            recent_k=1,
            questionnaire_title="mibs4"
        )



if __name__ == '__main__':
    print("Test Start")
    unittest.main()
