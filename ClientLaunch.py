# ClientLaunch.py
# Richard Parker
# Javier Cienfuegos Jr. 

import rpyc
def main():
  
  client = rpyc.connect("localhost", 18861) # Inherited Client 
  print("Connected")
  
  loggedin = False
  srvclient = client.root.QS()
            
  print("1 is for registering\n2 is for get quote\n3 is for get quote req name\n4 is for add quote\n")
    
  selection = raw_input("Select an option from above: ")
  
  # Registration
  if int(selection) == 1:
    name = raw_input("Please enter your name: ")
    if srvclient.register(name) == "OK":
      print("{0} registered!".format(name))
    else:
      print("{0} was not registered!".format(name))
      
  # Get Quote
  elif int(selection) == 2:
    get_quote = raw_input("Please enter your name: ")
    print(srvclient.get_quote(get_quote))
    
  # Gets Number of Requested Quotes
  elif int(selection) == 3:
    get_req_name = raw_input("Please enter your name: ")
    print("Number of Requested Quote by {0} is {1}".format(get_req_name, srvclient.quotes_requested(get_req_name)))
    
  # Add Quote
  elif int(selection) == 4:
    add_quote = raw_input ("Please enter your name: ")
    quote = raw_input("Please enter your quote: ")
    srvclient.add_quote(add_quote, quote)
    print("Quote added by {0}".format(add_quote))
    
  
main()
