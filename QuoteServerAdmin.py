# Quote Server Admin
# Richard Parker
# Javier Cienfuegos

class QuoteServerAdmin:
  
  def __init__(self, UQR, QUA):
    '''
    'UQR' represents the User Quote Request database file
    'QUA' represents the Quote User Add database file
    '''
    self.user_quotecount_file = UQR
    self.quote_useradd_file = QUA
    self.dict_uqr_db = {}
    self.dict_qua_db = {}
    
  def UserRequestedQuote(self, name):
    '''
    Changes the database file for the UQR and increments
    the quote request count.
    '''
    file_UQR = open(self.user_quotecount_file, 'r')
    lines = file_UQR.readlines()
    file_UQR.close()
    
    file_UQR = open(self.user_quotecount_file, 'w')
    for line in lines:
      if name in line.strip():
        file_UQR.write("{0};{1}\n".format(name, str(int(self.dict_uqr_db[name]) + 1)))
      else:
        file_UQR.write(line)
       
  def getUQRdb(self):
    '''
    Read in UQR file which is a CSV (Comma-Separated), which is the form
    of username;qreqcount where qreqcount is the request count of quotes from the user
    Return dictionary with (key,value) pair (username, qreqcount)
    '''
    file_UQR = open(self.user_quotecount_file, 'r')
    for line in file_UQR:
      self.dict_uqr_db[line.split(';')[0].strip()] = line.split(';')[1].strip()     
    file_UQR.close()
      
    return self.dict_uqr_db  
              
    
  def getQUAdb(self):
    '''
    Read in QUA file which is a CSV (Comma-Separted)
    of quote;username where 'quote' is the quote from string and
    'username' is the user who submitted it.username
    Return dictionary with (key,value) pair (quote, username)
    '''
    
    file_QUA = open(self.quote_useradd_file, 'r')
    for line in file_QUA:
      self.dict_qua_db[line.split(';')[0].strip()] = line.split(';')[1].strip()
      
    file_QUA.close()
    
    return self.dict_qua_db  
    
  def addQUAItem(self, name, quote):
    '''
    'name' is the username <String>
    'quote' is the quote <String> to be added to the quote database
    QUA file will be opened, the name and quote will be added to
    end of file, and the file will be closed. 
    '''
    
    with open(self.quote_useradd_file, "a") as file_QUA:
      file_QUA.write("{0};{1}\n".format(quote, name))
      
    file_QUA.close()
    
  def addUQRItem(self, name):
    '''
    'name' is the username <String>
    UQR file will be opened, the name will be added to the
    end of file, and the file will be closed.
    '''
    
    with open(self.user_quotecount_file, "a") as file_UQR:
      file_UQR.write("{0};{1}\n".format(name, '0'))
    
    file_UQR.close()
    