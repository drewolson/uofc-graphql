from dataclasses import dataclass
from typing import Any
import boto3
import graphene
import json


def call_lambda(client, function_name, request_payload={}):
    result = client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(request_payload),
    )

    return json.loads(result["Payload"].read())


@dataclass
class Context:
    lambda_client: Any


class Query(graphene.ObjectType):
    day_of_the_week = graphene.String(description="Current day of the week")
    random_number = graphene.Int(description="A random integer")

    def resolve_day_of_the_week(self, info):
        response = call_lambda(info.context.lambda_client, "uofc-current-time")

        return response.get("dayOfTheWeek")

    def resolve_random_number(self, info):
        response = call_lambda(info.context.lambda_client, "uofc-random")

        return response.get("number")


lambda_client = boto3.client("lambda")

schema = graphene.Schema(query=Query)


def lambda_handler(event, context):
    body = json.loads(event["body"])

    result = schema.execute(
        body.get("query"),
        context=Context(lambda_client),
    )

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(result.formatted),
    }
