import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello world')

    def resolve_hello(self, info):
        return 'World'


schema = graphene.Schema(query=Query)


def to_json(result):
    json = {"data": result.data}

    if result.errors != None:
        json["errors"] = result.errors

    return json


def handler(event, context):
    result = schema.execute(event.get("query"))

    return to_json(result)
