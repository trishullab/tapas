import os
import sys

class SimpleObservableProxyHTTPServer(MitmProxyHTTPServer):
        pass

class S(SocketServer.ThreadingMixIn, SimpleObservableProxyHTTPServer):
    pass

print 'Starting server on localhost:8080...'

srv = S(('localhost', 8080), H, sys.argv[1])
srv.serve_forever()
    return