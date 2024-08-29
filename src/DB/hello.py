import boto3
import mysql.connector
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials not found or incomplete.")
        raise e
    except Exception as e:
        print("Error retrieving secret from Secrets Manager.")
        raise e

    # Decrypts secret using the associated KMS key
    secret = get_secret_value_response['SecretString']
    
    return secret

# Secrets Managerからシークレットを取得
secret_name = "rds!cluster-80afcc80-d223-42eb-b4a4-2905fe01eb53"
region_name = "ap-southeast-2"
secret = get_secret(secret_name, region_name)

# シークレットはJSON形式で格納されていると仮定
import json
db_credentials = json.loads(secret)

# MySQLに接続
try:
    connection = mysql.connector.connect(
        host='your_db_endpoint',
        user=db_credentials['username'],
        password=db_credentials['password'],
        database='your_database_name'
    )
    print("Connected to the database!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        connection.close()
        print("Connection closed.")
