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

# AWS + API Orchestration

# Fin
