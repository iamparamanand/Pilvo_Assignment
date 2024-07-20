import requests
import os

SLACK_API_TOKEN = 'your_api_token'
SLACK_BASE_URL = 'https://slack.com/api'

headers = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}',
    'Content-Type': 'application/json'
}

def create_channel(name):
    url = f'{SLACK_BASE_URL}/conversations.create'
    data = {
        'name': name
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def join_channel(channel_id):
    url = f'{SLACK_BASE_URL}/conversations.join'
    data = {
        'channel': channel_id
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def rename_channel(channel_id, new_name):
    url = f'{SLACK_BASE_URL}/conversations.rename'
    data = {
        'channel': channel_id,
        'name': new_name
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def list_channels():
    url = f'{SLACK_BASE_URL}/conversations.list'
    response = requests.get(url, headers=headers)
    return response.json()

def archive_channel(channel_id):
    url = f'{SLACK_BASE_URL}/conversations.archive'
    data = {
        'channel': channel_id
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    channel_name = 'test-channel'
    new_channel_name = 'renamed-channel'
    
    # Create a new channel
    create_response = create_channel(channel_name)
    channel_id = create_response['channel']['id']
    print(f"Channel created: {create_response}")

    # Join the new channel
    join_response = join_channel(channel_id)
    print(f"Joined channel: {join_response}")

    # Rename the channel
    rename_response = rename_channel(channel_id, new_channel_name)
    print(f"Renamed channel: {rename_response}")

    # List all channels
    list_response = list_channels()
    print(f"List channels: {list_response}")

    # Archive the channel
    archive_response = archive_channel(channel_id)
    print(f"Archived channel: {archive_response}")
