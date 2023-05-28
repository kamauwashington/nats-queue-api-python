import asyncio
import settings
import signal
import sys
# IMPORTANT -> notice the .aio., this is usally written as 'from nats import NATS'
from nats.aio.client import Client as NATS 
from subscriberState import SubscriberState

# subscriber state manages information and actions pertinent to the executing process
sunsbcriberState = SubscriberState()


###################### DELAYED MESSAGE FUNCTIONALITY ######################

# this method executes an async delay for the duration defined in the environment variable : DURATION
async def delayedResponse(msg : NATS.msg_class) -> None :
    global subscriptionName

    # important to use await here, this is a non blocking sleep 
    await asyncio.sleep(settings.DURATION)

    messageCount : str = msg.data.decode()
    replyMessage : str = "Message %1s recieved by '%2s'." % (messageCount,subscriptionName)
    print(replyMessage)

    # using the Request-Reply pattern msg.respond publishes a message to the reply-to (message must be in bytes)
    await msg.respond(replyMessage.encode())


###################### SUBSCRIBER ######################

# this is the main subscriber, note that it is asynchronous as there are multiple awaits within needed by NATS
async def main () -> None : 
    print("Starting subscriber '%1s'." % (sunsbcriberState.getSubsriberName()))

    # provide access to the close connectionGlobal var for use in the keep alive loop
    #global closeConnection

    # NOTE - this is anycio compatible NATS, not the synchronous NATS functionality
    nc = NATS()

    # connect to the server defined in the environment variable : SERVER
    await nc.connect(servers=settings.SERVER)
    print("Connection to NATS Server '%1s' established by '%2s.'" % (settings.SERVER,sunsbcriberState.getSubsriberName()))
    
    # create the subscription to the subject defined in the environment variable : NATS_SUBJECT
    subscription = await nc.subscribe(
        settings.NATS_SUBJECT,

        # callback to the delayed response method defined above
        cb=delayedResponse,

        # IMPORTANT -> specifying queue allows multiple instances of this process to load balance
        # the queue specified in the environment variable : NATS_QUEUE_NAME.
        queue=settings.NATS_QUEUE_NAME
    )
   
    # while the global variable closeConnection is False, loop every one second to keep alive
    # this can be a larger amount if needed, it is set to 1 for quick exiting only
    while sunsbcriberState.hasOpenConnection() :
        await asyncio.sleep(1)
    

    ###################### CLEANUP and EXIT ######################
    
    # unsubscribe from the above NATS subscription
    await subscription.unsubscribe()
    print("\nUnsubscribed '%2s' from '%1s.'" % (settings.NATS_SUBJECT,sunsbcriberState.getSubsriberName()))

    # close the NATS connection, there have been instances where a process was not properly closed w/ orphan connections
    await nc.close()
    print("Closed connection to Nats Server '%1s'." % (settings.SERVER))

    # exit this process
    sys.exit()

# set the global closed to True to break the above while loop, and continue to CLEANUP and EXIT
def killProcess () -> None :
    sunsbcriberState.closeConnection()

# attach the killProcess script to SIGINT
signal.signal(signal.SIGINT, lambda sig,handler : killProcess() )

# asynchrnously run the subscription main function
asyncio.run(main())




