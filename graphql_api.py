from dataclasses import dataclass
from graphql.error import format_error
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


lambda_client = boto3.client("lambda")

schema = graphene.Schema(query=Query)


def to_json(result):
    data = result.formatted

    if data.get("errors") != None:
        data["errors"] = [format_error(error) for error in data["errors"]]

    return json.dumps(data)


def lambda_handler(event, context):
    body = json.loads(event["body"])

    result = schema.execute(
        body.get("query"),
        context=Context(lambda_client),
    )

    return {
        "statusCode": 200,
        "headers": {},
        "body": to_json(result),
    }
