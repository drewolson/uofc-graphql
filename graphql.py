import boto3
import graphene
import json

lambda_client = boto3.client("lambda")


class Query(graphene.ObjectType):
    hello = graphene.String(description="A typical hello world")
    number = graphene.Int(description="A random integer")

    def resolve_hello(self, info):
        return 'World'

    def resolve_number(self, info):
        result = lambda_client.invoke(
            FunctionName="uofc-random",
            Payload="",
        )

        payload = json.loads(result["Payload"].read())

        return payload.get("number")


schema = graphene.Schema(query=Query)


def to_json(result):
    json = {"data": result.data}

    if result.errors != None:
        json["errors"] = result.errors

    return json


def lambda_handler(event, context):
    result = schema.execute(event.get("query"))

    return to_json(result)
