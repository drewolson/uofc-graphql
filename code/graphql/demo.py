from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
import graphene
import requests


# start snippet helpers
def random_number():
    return randrange(0, 10)

def day_of_the_week():
    response = requests.get(
        "http://worldclockapi.com/api/json/cst/now"
    )
    body = response.json()

    return body.get("dayOfTheWeek")
# end snippet helpers

# start snippet query
class Query(graphene.ObjectType):
    day_of_the_week = graphene.String()
    random_number = graphene.Int()

    def resolve_day_of_the_week(self, info):
        return day_of_the_week()

    def resolve_random_number(self, info):
        return random_number()
# end snippet query


schema = graphene.Schema(query=Query)

# start snippet fastapi
app = FastAPI()

class GraphQLRequest(BaseModel):
    query: str

@app.post("/")
def index(request: GraphQLRequest):
    result = schema.execute(
        request.query,
    )

    return result.formatted
# end snippet fastapi
