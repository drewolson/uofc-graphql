from dataclasses import dataclass
from typing import Any
import boto3
import graphene
import json


@dataclass
class Context:
    lambda_client: Any


class Query(graphene.ObjectType):
    ping = graphene.String(description="Pong")
    number = graphene.Int(description="A random integer")

    def resolve_ping(self, info):
        return "pong"

    def resolve_number(self, info):
        result = info.context.lambda_client.invoke(
            FunctionName="uofc-random",
            Payload="",
        )

        payload = json.loads(result["Payload"].read())

        return payload.get("number")


def to_json(result):
    json = {"data": result.data}

    if result.errors != None:
        json["errors"] = result.errors

    return json


lambda_client = boto3.client("lambda")

schema = graphene.Schema(query=Query)


def lambda_handler(event, context):
    result = schema.execute(
        event.get("query"),
        context=Context(lambda_client),
    )

    return to_json(result)
