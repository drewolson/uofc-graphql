from fastapi import FastAPI
from pydantic import BaseModel
import graphene

# start snippet query
class Greeting(graphene.ObjectType):
    hello = graphene.String()
    goodbye = graphene.String()

class Query(graphene.ObjectType):
    greeting = graphene.Field(
        Greeting,
        name=graphene.String(required=True),
    )

    def resolve_greeting(self, info, name):
        return {
            "hello": f"Hello, {name}!",
            "goodbye": f"Goodbye, {name}!",
        }
# end snippet query


schema = graphene.Schema(query=Query)

app = FastAPI()

class GraphQLRequest(BaseModel):
    query: str

@app.post("/")
def index(request: GraphQLRequest):
    result = schema.execute(
        request.query,
    )

    return result.formatted
