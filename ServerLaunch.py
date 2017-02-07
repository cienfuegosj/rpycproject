# ServerLaunch.py   
# Launch the server
from QuoteServer import QuoteServer

if __name__ == "__main__":
  '''
  This is a threaded server. Note that servers can run concurrently,
  but I don't know if the Python Module allows it to run in sync.
  '''
  from rpyc.utils.server import ThreadedServer
  t = ThreadedServer(QuoteServer, port=18861)
  print("Launching the Server")
  t.start()
  