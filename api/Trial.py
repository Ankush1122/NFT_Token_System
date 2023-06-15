import requests

endpoint = "http://0.0.0.0:8080/api/"


get_response = requests.post(endpoint, data={'difficulty':'3'})
print(get_response.json())