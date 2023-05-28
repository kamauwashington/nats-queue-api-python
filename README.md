# Nats.io Queue Group as Sanic REST API in Python3+

> This repository is purely for reference and is illustrative in it is purpose. Please do not use in production as is, use this as a guide
or starting point for a production level implementation.


This project illustrates the use of [Nats.io](https://nats.io/) built in [Queue Group/Subscription load balancing streaming pattern](https://docs.nats.io/nats-concepts/core-nats/queue) within an [Sanic](https://sanic.dev/en/) API. The goal behind this implementation is to showcase a loosely coupled pub-sub Rest API Queue Group/Subscription pattern, wherein the implementation of an API request is handled by multiple subscribers in a load balanced fashion with one request sent to one subscriber in a pool of subscribers. This is different than the basic pattern where a message is sent to *All* subscribers.

> Think of NATS Queue Groups as pools of subscribers that load balance incomming subject messages independetly with no knowledge of other subscribers in the pool. This allows a subscriber to scale itself to meet demand.


> What will be seen in this example is an API that recieves requests through Sanic, sends the message-id to a NATS subject, and a Queue Group effectively
load balancing the incoming requests. Performance improvements can be seen by adding additional subscribers, without modifiying the API (note, the API can be scaled as well)

## Prerequisites

Before you continue, ensure you have met the following requirements:

* [Nats Server](https://docs.nats.io/running-a-nats-service/introduction/installation#downloading-a-release-build) or [Nats Docker Server](https://hub.docker.com/_/nats) installed and running
    * If installing the Go Server, [Go](https://go.dev/doc/install) must be installed
* Python3+
* Pip3 23+
* **OPTIONAL**
    * **[Artillery](https://www.npmjs.com/package/artillery)** can be used to run load tests (install globally)
        * **NOTE** If there is another preference for load testing, Artillery will not be needed
        * NodeJS v18 or higher installed
        * Npm installed

## Environment Variables

This repository uses dotenv, feel free to create a .env file to set the ALPHA_VANTAGE_KEY, or override other aspects of the program.

* HOST : The host of the Sanic server (defaults to **localhost**)
* HOST_PORT : The port the Sanic server should run on (defaults to **8000**)
* SUBJECT : The Nats subject the Request/Reply will be issued on (defaults to **stock.request**)
* NATS_SERVER : The Nats server that will be facilitating Pub-Sub (defaults to  **localhost**)
* DURATION : The time in seconds the subscriber should run for before returning a result (defaults to **100ms** or **.100**) 
* NATS_QUEUE_NAME : The name of the queue that the subscribers will use to for a Queue Group (defaults to **nats_default_queue**)

## Running the Application

1) 'cd' to the root of this repository (where it was cloned)
1) **OPTIONAL** Create a file in the root named **.env**
    * Enter values for any of the above environment variables to be changed
1) run **pip3 install -r requirements.txt** from the command line
1) run **python3 api.py** from the command line
1) open a **NEW** terminal to the root of this repository and run **python3 subscriber.py** 
    * _allow the subscription a few additional seconds to bind, 503 errors may be experienced during this binding time_
    * Messages similar to the following should display :
        > Starting subscriber 'wine-rooster'. Connection to NATS Server 'localhost' established by 'wine-rooster'. Where 'wine-rooster' is the generated name given to the open subscription 
1) open Postman or a browser and execute a GET request to : 
    * **http://localhost:8000** or **http://< HOST > :< HOST_PORT >** as defined in .env
    * the response should look like :
        > *Message 19 recieved by 'wine-rooster'.* where 'wine-rooster' is the generated name given to the open subscription
1) Repeat steps 5 and 6 opening a **NEW** terminal for the subscription  (issued at the root of this repository)
    > It can be observed that there will be responses from other subscriptions as such : *Message 9 recieved by 'macho-baboon'.* where 'macho-baboon' is the generated name given to the open subscription
1) As these processes are started (remember to run each in its own terminal/console), it can be observed that subscribers are randomply selected from the Queue Group for message processing, effectively load balancing the subject requests.
1) **OPTIONAL** run load tests with Artillery. This is a surefire way to observe the performance improvement and load balancing capability
    * open a new terminal to the project root and run **artillery quick --count 20 -n 20 http://127.0.0.1:8000/ --output report.json && artillery report report.json**

## What am I Seeing?

A REST API that is only aware of a Nats Subject, and that it is the publisher. (n) amount of Request-Reply subscribers in a Queue Group are load balancing requests to the defined NATS Subject.

## Notes
* Notice that the API has no prior knowledge as to what the subscribers are going to provide, nor how many there will be
* This repository is heavily commented to provide context as to what and why, if in VS Code feel free to collapse all comments if they are obtrusive
    * On Mac -> Press <kbd>&#8984;</kbd> + <kbd>K</kbd> then <kbd>&#8984;</kbd> + <kbd>/</kbd> 
    * On Windows & Linux -> Press <kbd>Ctrl</kbd> + <kbd>K</kbd> then <kbd>Ctrl</kbd> + <kbd>/</kbd> 

## Try!
* adding additional subscribers and observe the results. When is the point where there are too many subscribers and performance starts to degrad?
* adding additional non-reply subscribers, that perform other duties based on data passed in via JSON instead of empty data
* writing a subscriber in Go|Java|.NET Core|Python, and observe the results
* writing the REST api in Go|Java|.NET Core|Python, and observe the results