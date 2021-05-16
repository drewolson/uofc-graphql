from fastapi import FastAPI
from random import randrange
import requests


# start snippet random
def random_number():
    return randrange(0, 10)
# end snippet random


# start snippet day
def day_of_the_week():
    response = requests.get(
        "http://worldclockapi.com/api/json/cst/now"
    )
    body = response.json()

    return body.get("dayOfTheWeek")
# end snippet day

# start snippet fastapi
app = FastAPI()

@app.get("/")
def index():
    return {
        "number": requests
                    .get("http://random.service")
                    .json()
                    .get("number"),
        "dayOfTheWeek": requests
                    .get("http://day-of-the-week.service")
                    .json()
                    .get("number"),
    }
# end snippet fastapi
