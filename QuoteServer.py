# Quote Server
# Richard Parker
# Javier Cienfuegos

import rpyc
import random 
from QuoteServerAdmin import QuoteServerAdmin

class QuoteServer(rpyc.Service):
  
  def on_connect(self):
     pass
  def on_disconnect(self):
     pass
    
  class exposed_QS:
    def __init__(self):
      '''
      Create the Quote Server Administrator that will allow us to pull dictionaries
      that have the database information.
      '''     
         
      self.DBAdmin = QuoteServerAdmin("Database/UQRdb.txt", "Database/QUAdb.txt")
      self.dict_UQR = self.DBAdmin.getUQRdb()
      self.dict_QUA = self.DBAdmin.getQUAdb()
     
    def exposed_register(self, name):
      '''
      'name' is the username <String>
      Checks the U-QR database if the username is registered and
      adds it to the database if unique.
      Return: "OK" if database is updated correctly, "KO" if error.
      '''
      self.dict_UQR = self.DBAdmin.getUQRdb() # Update
      print("Registering {0}...".format(name))
      if name not in self.dict_UQR.keys():
        self.DBAdmin.addUQRItem(name)
        return "OK"
      else:
        return "KO"
    
    def exposed_get_quote(self, name):
      '''
      'name' is the username <String>
      Checks if the user is a valid user in the U-QR database.
      Returns random quote <String> from QUA database if valid user.
      Otherwise, raise error.
      '''
      print("Getting quote for {0}...".format(name))
      self.dict_QUA = self.DBAdmin.getQUAdb() # Update
      if name in self.dict_UQR.keys():
        self.DBAdmin.UserRequestedQuote(name)
        return random.choice(self.dict_QUA.keys())
      else:
        raise ValueError("Invalid username. Try a different username.")
    
    def exposed_quotes_requested(self, name):
      '''
      'name' is the username <String>
      Checks if the user is a valid user in the U-QR database.
      Returns number of quotes requested from the user if valid user.
      Otherwise, raise error.
      '''
      print("Returning number of quotes requested for {0}...".format(name))
      self.dict_UQR = self.DBAdmin.getUQRdb() # Update
      if name in self.dict_UQR.keys():
        return self.dict_UQR[name]
      else:
        raise ValueError("Invalid username. Try a different username.")
    
    def exposed_add_quote(self,name, quote):
      '''
      'name' is the username <String>
      'quote' is the quote to be added to the U-QR database. 
      Checks if the user is a valid user in the U-QR database.
      If valid, place the quote in the U-QR database with the corresponding
      username. 
      '''
      print("Adding quote to database...")
      if name in self.dict_UQR.keys():
        self.DBAdmin.addQUAItem(name, quote)
        self.dict_QUA = self.DBAdmin.getQUAdb() # Update
      else:
        raise ValueError("Invalid username. Try a different username.")
  
  