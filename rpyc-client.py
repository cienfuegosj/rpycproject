import rpyc

client = rpyc.connect("localhost", 18861)

response = client.root.say_hi()

print(response)