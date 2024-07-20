import csv
import requests
import os

PLIVO_AUTH_ID = 'your_auth_id'
PLIVO_AUTH_TOKEN = 'your_auth_token'
PLIVO_BASE_URL = 'https://api.plivo.com/v1/Account/'

def create_customer_message_csv():
    with open('data/customer_message.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'SourceNumber', 'DestinationNumber', 'Message'])
        writer.writerows([
            [1, 'src', 'dst1', 'Sending the SMS to customer ID 1'],
            [2, 'src', 'dst2', 'Sending the SMS to customer ID 2'],
            [3, 'src', 'dst3', 'Sending the SMS to customer ID 3'],
            [4, 'src', 'dst4', 'Sending the SMS to customer ID 4']
        ])

def send_sms(src, dst, text):
    url = f'{PLIVO_BASE_URL}/{PLIVO_AUTH_ID}/Message/'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'src': src,
        'dst': dst,
        'text': text
    }
    response = requests.post(url, json=data, auth=(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN), headers=headers)
    return response.json()

def read_and_send_sms(customer_ids):
    with open('data/customer_message.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ID']) in customer_ids:
                response = send_sms(row['SourceNumber'], row['DestinationNumber'], row['Message'])
                with open('results/result.txt', mode='a') as result_file:
                    result_file.write(f"Sent SMS to {row['ID']}: {response}\n")

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    create_customer_message_csv()
    customer_ids = list(map(int, input("Enter customer IDs (comma separated): ").split(',')))
    read_and_send_sms(customer_ids)
