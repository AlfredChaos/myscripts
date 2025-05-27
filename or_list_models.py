import requests

url = "https://openrouter.ai/api/v1/models"

response = requests.get(url)

print(response.json())
