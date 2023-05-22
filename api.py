from sanic import Sanic, Request
from sanic.response import text
# IMPORTANT -> notice the .aio., this is usally written as 'from nats import NATS'
from nats.aio.client import Client as NATS 
import settings
import asyncio


# create the Sanic application
app : Sanic = Sanic("NatsQueueAPI")
app.config.REQUEST_TIMEOUT = 10


###################### ON BEFORE APPLICATION START ######################

# this method will run before the application is started, to initialize context data
@app.before_server_start
async def onBeforeStart(app : Sanic, _) -> None :
    
    # NOTE - this is anycio compatible NATS, not the synchronous NATS functionality
    nc = NATS()

    # connect to the server defined in the environment variable : SERVER
    await nc.connect(servers=settings.SERVER)
    print("Connection to NATS Server '%1s' established." % (settings.SERVER))

    # set NATS connection on the Sanic context so that it can be used in the async scope of the application
    # there is an option on app.ext to register a typed object (this would be more than likely preferred)
    app.ctx.nc = nc

    # this count will be used as an auto increment identifying messages being load balanced across subscribers
    app.ctx.messageCount : int = 0


###################### API "/" ROOT ENDPOINT (GET) ######################

# basic root endpoint http://<HOST>:<HOST_PORT> (defaults to http://localhost:8000)
@app.get("/")
async def root_request(request : Request):
    try:
       
        # increment the message count (to identify messages when multiple subscribers are attached)
        app.ctx.messageCount += 1

        # use NATS Request/Reply pattern to publish to NATS_SUBJECT (it should be load balanced and sticky to the receiving subscriber)
        msg : NATS.msg_class = await app.ctx.nc.request(settings.NATS_SUBJECT, str(app.ctx.messageCount).encode(),timeout=60)

        # return the subscriber response to the requestor (message returned is in bytes must decode to utf-8)
        return text(msg.data.decode())

    except asyncio.TimeoutError:

        # there should not be timeouts unless a large duration is set
        print("Timed out waiting for response")
        return text("Request timed out sending message %1s." % (app.ctx.messageCount))


###################### ON BEFORE APPLICATION CLOSE ######################

# this method will run before the application is stopped, in which the connection to NATS can be closed to prevent orphan connections
@app.before_server_stop
async def onBeforeStop(app, _) -> None :

    # the NATS connection when attempting to close should use the 'await' keyword to operate properly
    await app.ctx.nc.close()
    print("\nConnection to NATS Server '%1s' closed." %  (settings.SERVER))


# default main function to start Sanic application
def main() -> None :
    app.run(host=settings.HOST, port=int(settings.HOST_PORT))


if __name__ == '__main__':
    main()
