from fastapi import FastAPI
from pydantic import BaseModel
import graphene


# start snippet query
class Query(graphene.ObjectType):
    ping = graphene.String()

    def resolve_ping(self, info):
        return "pong"
# end snippet query


# start snippet fastapi
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
# end snippet fastapi
