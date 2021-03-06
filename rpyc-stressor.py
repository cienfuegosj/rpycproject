# -*- coding: utf-8 -*-
# Invoke using
# python rpyc-stressor≥py 0 0 30 10
# which would mean
# run this with an index of zero, a number of processes as zero
# (both of those numbers are meaningless if you call this script
# directly), and run 30 users with 10 requests each.

import random, \
       rpyc, \
       sys, \
       time, \
       datetime 

# Setup Google Sheets API and Authentication
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
# Creates a Google Spreadsheets Client with the proper JSON credentials
gc = gspread.authorize(credentials)
sh = gc.open('Testing Spreadsheet')
#sh = gc.create('Testing Spreadsheet {0}'.format(str(datetime.datetime.now())))
sh.share('cienfuegoseveryday@gmail.com', perm_type='user', role='owner')
worksheet = sh.get_worksheet(0)

# Grab a connection to the server
# Local VM Server
# client = rpyc.connect("localhost", 18861)
# Asia VM Server
client = rpyc.connect("104.199.179.195",8888)
srvclient = client.root.QS()

# The "root" is the class we registered with the server.
# So, all exposed methods can be called off of the "root".

# I generate random usernames. These are the bases for 
# those random usernames.
usernames = ["alpha", "bravo", "charlie", "delta", \
             "echo", "foxtrot", "golf", "hotel", \
             "india", "juliet", "kilo", "lima", "motel", \
             "november", "oscar", "papa", "quebec", \
             "romeo", "sierra", "tango", "uniform", "victor", \
             "whiskey", "xray", "yankee", "zulu"
            ]

# This keeps track of the names of the users I generate.
# For a brief moment, I think I cared about this.
# Ultimately, I stopped caring about this. But, the code remains.
users_genned = []

# These are the timings for the request loops.
request_times = []

# These are names given to the inputs to the script.
# The script takes four parameters on the command line.
# The run_index is in conjunction with the Bash script...
#    it tells me which # this is when they are running in parallel.
# The num_processes tells me how many simultaneous scripts were running
#    when this data was generated. Handy when you start doing a lot of testing.
#    I print this so I can keep track, otherwise I'd forget.
# The other two are self-explanatory: they're how many users we're going
#    to generate, and how many requests each user will make.
# This script runs these users (and their requests) in sequence.
# We have to run multiple copies of the script in parallel to get any 
# real stress-testing of our server.
run_index     = int(sys.argv[1])
num_processes = int(sys.argv[2])
num_users     = int(sys.argv[3])
num_req       = int(sys.argv[4])

# Start timing how long the whole loop takes.
all_start = time.time()
for i in range(0, num_users):
  # Generate a random username. For all I know, this violates my requirements
  # about what makes a valid username...
  user = "{0}{1}".format(random.choice(usernames), random.randint(0, 100))
  # Keep track of the username I just generated.
  users_genned.append(user)
  # Register the user. This looks just like the client script.
  srvclient.register(user)
  # Add a quote from this user. It is a boring quote.
  srvclient.add_quote(user, "This is quote {1} from {0}.".format(user, i))
  
  # Start timing the requests that this user makes.
  requests_start = time.time()
  # Make however many requests we indicated on the command line.
  for j in range(0, num_req):
    # Get a quote. Don't print it, or we'll be timing how long
    # it takes to print. On a cloud sever, that means timing how long
    # it takes the characters to be transmitted over the network to my local
    # terminal... we don't want to time that.
    srvclient.get_quote(user)
  # Stop timing the request loop.
  requests_end = time.time()
  # Append the time it took to make these requests to the list of loop
  # timings. Note this append adds to the total loop time... and, we can't 
  # avoid that. Fortunately, the append is probably *very* fast compared
  # to the network calls. That said, it is padding out our timing.
  request_times.append(requests_end - requests_start)
# Stop timing the whole loop.
all_end = time.time()

# Calculate the total time spent in stress-testing
all = all_end - all_start
# Calculate the average. Remember, we are timing loops with multiple
# requests, so the actual average per request will be the average of 
# the times divided by the number of requests.
average = (sum(request_times) / len(request_times)) / num_req
# As we discovered, those two extra network calls made a huge difference.
# We can't leave any network calls out of our timing calculations...
rps = (num_users * (num_req + 2)) / all
# Print the data. If you want to get fancy, you could generate a timestamp
# and use it to store the data in a file. We'll do that for our 
# next server test.

worksheet.append_row([run_index, num_processes,num_users, num_req, all, average, rps, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])
print("{0},{1},{2},{3},{4},{5},{6}".format(run_index, num_processes, num_users, num_req, all, average, rps))
