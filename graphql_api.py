from dataclasses import dataclass
from typing import Any
import boto3
import graphene
import json


@dataclass
class Context:
    lambda_client: Any


class Query(graphene.ObjectType):
    day_of_the_week = graphene.String(description="Current day of the week")
    random_number = graphene.Int(description="A random integer")

    def resolve_day_of_the_week(self, info):
        result = info.context.lambda_client.invoke(
            FunctionName="uofc-current-time",
            Payload="",
        )

        payload = json.loads(result["Payload"].read())

        return payload.get("dayOfTheWeek")

    def resolve_random_number(self, info):
        result = info.context.lambda_client.invoke(
            FunctionName="uofc-random",
            Payload="",
        )

        payload = json.loads(result["Payload"].read())

        return payload.get("number")


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
