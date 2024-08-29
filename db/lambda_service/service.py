import boto3
import psycopg2
import argparse
from time import sleep

lambda_client = boto3.client('lambda', region_name='us-west-2')

conn = psycopg2.connect(
    dbname="lambda_data",
    user="admin",
    password="password123",
    host="your-rds-endpoint",
    port="5432"
)

def call_lambda_and_store():
    response = lambda_client.invoke(
        FunctionName='grpc-scrape-lambda',
        InvocationType='RequestResponse'
    )
    payload = response['Payload'].read().decode('utf-8')

    with conn.cursor() as cur:
        cur.execute("INSERT INTO responses (data) VALUES (%s)", (payload,))
        conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type=int, default=60)
    args = parser.parse_args()
    while True:
        call_lambda_and_store()
        sleep(args.interval)

