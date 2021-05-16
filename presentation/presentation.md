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

1. Generates a random number between 1 and 10
2. Returns the current day of the week

## API Orchestration

We can build an API Orchestration layer that provides the capabilities of each
of these services by delegating to them in order to generate an API response to
our user.

## API Orchestration

```plantuml
[HTTP Request]

[API Orchestration]

node services {
  [Random Number]
  [Day of the Week]
}

[HTTP Request] -down-> [API Orchestration]
[API Orchestration] -down-> [Random Number]
[API Orchestration] -down-> [Day of the Week]
```

# GraphQL

# AWS + API Orchestration

## Another Slide

Some content

. . .

More after a pause

## A Slide with Code

```{.python include=../code/aws_demo/graphql_api.py}
```

# Fin
