# this will be used to generate human readable names for each subscription
from coolname import generate_slug

# Using a class to handle out of scope variables or functionality as asyncio is used.
# This is one of the Python ways of avoiding globals, and or providing "global-like" functionality
class SubscriberState :
    def __init__(self) :
        # this property is used to control the loop keeping the wait state open to recieve messages
        self._open : bool = True
        # generate a coolname for this subscriber
        self._subscriberName : str = generate_slug(2)

    # this method will be used to top the iteration that keeps the subscriber open
    # a .wait() method could be added here to keep the connection alive as well
    def closeConnection(self) -> None :
        self._open = False
    
    
    # identifies if the subscriber state is stile alive
    def hasOpenConnection(self) -> bool :
        return self._open
    
    # returns the name of the subscriber process
    def getSubsriberName(self) -> str :
        return self._subscriberName