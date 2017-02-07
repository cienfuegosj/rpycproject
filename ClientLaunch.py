# ClientLaunch.py
# Javier Cienfuegos Jr. 

import rpyc
def main():
  
  client = rpyc.connect("localhost", 18861) # Inherited Client 
  print("Connected")
  
  loggedin = False
  
  while loggedin == False:
    password = raw_input("Please enter the database password: ")
    try:
      srvclient = client.root.QS(password)
      loggedin = True
      print("Logged in!")
    except ValueError:
      print(ValueError)
    
  # Register 
  
  if srvclient.register("heannie") == "OK":
    print("Registration went perfect!")
  else:
    print("Could not be registered. Sorry.")
    
  print(srvclient.get_quote("cienfuegosj"))
  
main()
