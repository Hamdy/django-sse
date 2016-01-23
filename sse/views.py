from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponse
import json
import time
from datetime import datetime

def home(request):
    return render(request, 'home.html', {})


def sse(request):
    def itero():
        """
            In all cases the connection is set to keep-alive
            (request header)
            
            Connection:keep-alive
            
            so it's a live until finishes
                
            - Data returned could be saved in client side js dict/object allowing for real-time
            charts in client side
            say data in the past 5 minutes are saved in dict and thus allowing for real-time charts
            we can even better save those data in local storage (5mb per app)
            and use them ;for realtime charts
        
            return format: (Blank lines are required)
            
            --- Snip----
            retry: 2000


            event: message
            data: {"time": "2014-08-21 21:44:37.524461"}

            ---End---
            
            
            No POST supported in SSE, so in order to do some kind of login
            and u don't want to use GET coz user and pass will end up in 
            URL and eventually in Log files and such stuff
            
            Use cookies to put login data and send the GET request to server and 
            let server side taks care of this
            
        """
        # this thing finishes instantly and depending on the retry rate, the receiver will retry this again
        # in js code
        # es.onerror , the   (event.target.readyState) will always be 0 or connecting
        # as this is one quick connection and ends fast
        # this should be inside a for loop that sleeps a second then sends the data
        s = """retry: 2000\n\nevent: message\ndata: gg\n\n"""
        data = json.dumps({'time':str(datetime.now())})
        s = '\n'.join(['retry: 1000', '\n', 'event: message', 'data: %s' % data, '\n'])
        yield s
        
        ####
        
        
        # Hold one long connection, that pushes number from 0 to 9 every second
        # after finishing, the request the loop/ request will be repeated again instantly
        # ad the retry time is small 
        # so we'll have another long conenction from 0-9 then another and so on
        for i in range(10):
            s = '\n'.join(['retry: 1000', '\n', 'event: message', 'data: %s' % i, '\n'])
#             time.sleep(1)
#             yield s

        # one ling connection fronm 0-9 then wait until retry time passes
        # before another request is issued and since rerty time is big, the 2nd request will
        # be issued after thie time
        for i in range(10):
            s = '\n'.join(['retry: 100000', '\n', 'event: message', 'data: %s' % i, '\n'])
#             time.sleep(1)
#             yield s
        
        # heart beat (thid only triggers the message event wow)
        s = 'data:\n\n'
#         yield s


        # heartbeat 2 (doesn't trgiger message event
        s = ':\n\n'
#         yield s

        # heartbeat
        """
            Heartbeat/keep a live signal  is to ensure that socket stays a live
            and not dead, coz some browsers or proxies even may kill socket if
            socket is idle for a while, and we don't want this to happen 
            SSE has reconnect function, if socket killed cleanly, browser will
            try to re-connect but this is if socket is killed cleanly
            yet in reallife it may take browser up to 120 seconds to detect
            a dead socket.
            So this mechanism is not reliable in keeping connection open
        """

    
    if request.META.get('HTTP_ACCEPT') == 'text/event-stream':
        response = StreamingHttpResponse(itero(), content_type="text/event-stream")
    else:
        response = HttpResponse("http") 
    return   response