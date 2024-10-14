import requests

# Replace with your actual Roboflow API key
API_KEY = 'tJUOl22WsAVuNvN5vkhu'
BASE_URL = 'https://api.roboflow.com'

# Set up the headers with your API key
headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# Make the GET request to fetch workspaces
response = requests.get(f'{BASE_URL}/workspaces', headers=headers)

# Check if the request was successful
if response.status_code == 200:
    workspaces = response.json()
    print("Available Workspaces:")
    for workspace in workspaces['workspaces']:
        print(f"- {workspace['name']} (ID: {workspace['id']})")
else:
    print(f"Failed to fetch workspaces: {response.status_code} - {response.text}")
