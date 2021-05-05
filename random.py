from random import randrange


def lambda_handler(event, context):
    return {"number": randrange(0, 10)}
