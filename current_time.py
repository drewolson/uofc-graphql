import requests


def lambda_handler(event, context):
    response = requests.get("http://worldclockapi.com/api/json/cst/now")

    return response.json()
