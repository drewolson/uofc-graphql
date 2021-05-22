---
title: API Orchestration in the Cloud
subtitle: It's just regular API Orchestration
date: May 24th, 2021
author: Drew Olson
theme: metropolis
---


## About Me

Hi, I'm Drew Olson

* Chief Architect at GoFundMe
* Previously Chief Architect at Braintree
* https://drewolson.org

# Agenda

## Agenda

* API Orchestration
* GraphQL
* AWS + API Orchestration

# API Orchestration

## API Orchestration

API Orchestration is about decoupling your API from your architectural
decisions.

## API Orchestration

We'd like to expose a simple, coherent API to our users regardless of how we
choose to build the service(s) that power our application.

## API Orchestration

Suppose we have two simple services within our application:

1. Generate a random number between 0 and 9
2. Return the current day of the week

## API Orchestration

We can build an API Orchestration layer that provides the capabilities of each
of these services by delegating to them and composing their responses as an API
response to our user.

## API Orchestration

```plantuml
skinparam dpi 300

cloud {
  () "HTTP Request"
}

[API Orchestration]

node services {
  [Random Number]
  [Day of the Week]
}

() "HTTP Request" -down-> [API Orchestration]
[API Orchestration] -down-> [Random Number]
[API Orchestration] -down-> [Day of the Week]
```

## API Orchestration

Let's assume initially these "services" are just functions within our
application (please never start with microservices). We can build this
"orchestration layer" quite simply.

## API Orchestration

Here's our `random_number` function:

```{.python include=../code/orchestration/simple.py snippet=random}
```

## API Orchestration

Here's our `day_of_the_week` function:

```{.python include=../code/orchestration/simple.py snippet=day}
```

## API Orchestration

Because this code exists locally, our API orchestration layer is very simple:

. . .

```{.python include=../code/orchestration/simple.py snippet=fastapi}
```

## API Orchestration

```
$ curl localhost:8000
{"number":9,"dayOfTheWeek":"Sunday"}%
```

## API Orchestration

If we eventually chose to extract `random_number` and `day_of_the_week` to
separate services, our orchestration layer gets more complicated.

## API Orchestration

```{.python include=../code/orchestration/complicated.py snippet=fastapi}
```

## API Orchestration

Now we're making two HTTP requests to downstream services.

. . .

If one service call fails, the whole API request fails.

. . .

If either service call is expensive, we pay this penalty for every API request.

## API Orchestration

We can do better.

# GraphQL

## GraphQL

**GraphQL** is a specification for an API query language and a set of executor
libraries written in several languages.

## GraphQL

**GraphQL** is *not*:

* A database
* A serialization format
* Super complicated

## GraphQL

Our clients make a JSON request to our server in the following format:

```json
{
  "query": "<graphql query>"
}
```

## GraphQL

We pass the query to an executor, which returns a response in the following
format:

```json
{
  "data": { ... },
  "errors": null | [{ ... }]
}
```

## GraphQL - Hello world

We'll be using `python`'s `graphene` library to execute our GraphQL queries.

## GraphQL - Hello world

```{.python include=../code/graphql/simple.py snippet=query}
```

## GraphQL - Hello world

And we'll use `fastapi` to accept queries via HTTP + JSON. This code never
changes across our examples.

## GraphQL - Hello world

```{.python include=../code/graphql/simple.py snippet=fastapi}
```

## GraphQL - Hello world

We can now make an HTTP request with the following query:

```graphql
{
  ping
}
```

```
$ curl -X POST -d '{"query": "{ ping }"}' localhost:8000
{"data":{"ping":"pong"},"errors":null}%
```

## GraphQL - Providing Arguments

```{.python include=../code/graphql/args.py snippet=query}
```

## GraphQL - Providing Arguments

Request:

```graphql
{
  hello(name: "Drew")
}
```

Response:

```json
{
  "data": {
    "hello":"Hello, Drew!"
  },
  "errors":null
}
```

## GraphQL - Nested Fields

```{.python include=../code/graphql/nested.py snippet=query}
```

## GraphQL - Nested Fields

Request:

```graphql
{
  greeting(name: "Drew") {
    hello
    goodbye
  }
}
```

## GraphQL - Nested Fields

Response:

```json
{
  "data": {
    "greeting": {
      "hello": "Hello, Drew!",
      "goodbye": "Goodbye, Drew!"
    }
  },
  "errors": null
}
```

## GraphQL - Our Example

```{.python include=../code/graphql/demo.py snippet=helpers}
```

## GraphQL - Our Example

```{.python include=../code/graphql/demo.py snippet=query}
```

## GraphQL - Our Example

Request:

```graphql
{
  randomNumber
  dayOfTheWeek
}
```

## GraphQL - Our Example

Response:

```json
{
  "data": {
    "randomNumber": 6,
    "dayOfTheWeek": "Saturday"
  },
  "errors": null
}
```

## GraphQL

BUT WAIT THERE'S MORE!

. . .

In GraphQL, the server will only resolve the **fields you ask for**. This means
if you only ask for `randomNumber`, the server **will not** make an external
HTTP request to fetch the current day.

## GraphQL

Request:

```graphql
{
  randomNumber
}
```

## GraphQL

Response:

```json
{
  "data": {
    "randomNumber": 8
  },
  "errors": null
}
```

## GraphQL

Client-driven responses allow our orchestration layer to be far more efficient.
We do only the work required to return the **exact fields** our client requests.

. . .

This is especially important if each of our fields is resolved by calling
another service.

## GraphQL

GraphQL also gives us **partial responses** for free.

. . .

This means that if we fail to resolve one of our fields but succeed in resolving
a second, we will send the client the data we were able to resolve and an error
representing the failure.

. . .

A single resolution failure **does not** fail the whole request.

# AWS + API Orchestration

## "Cloud" Orchestration

We're going to implement an orchestration layer identical to our first demo, but
using AWS's API Gateway and Lambda.

## "Cloud" Orchestration

```plantuml
skinparam dpi 300

cloud {
  () "HTTP Request"
}

[API Gateway]

[GraphQL (Lambda)]

node services {
  [Random Number (Lambda)]
  [Day of the Week (Lambda)]
}

() "HTTP Request" -down-> [API Gateway]
[API Gateway] -down-> [GraphQL (Lambda)]
[GraphQL (Lambda)] -down-> [Random Number (Lambda)]
[GraphQL (Lambda)] -down-> [Day of the Week (Lambda)]
```

## "Cloud" Orchestration

LIVE DEMO THAT I HOPE WON'T FAIL!

## Wrap Up

Final points:

* GraphQL is great for API orchestration

. . .

* Presentation and code -- https://github.com/drewolson/uofc-graphql

. . .

* You should learn to play bridge

. . .

* You should learn Haskell

# Thanks! Questions?
