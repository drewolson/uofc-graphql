from fastapi import FastAPI
from pydantic import BaseModel
import graphene


# start snippet query
class Query(graphene.ObjectType):
    hello = graphene.Field(
        graphene.String,
        name=graphene.String(required=True),
    )

    def resolve_hello(self, info, name):
        return f"Hello, {name}!"
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
