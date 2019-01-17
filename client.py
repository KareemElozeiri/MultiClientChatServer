import socket


host = '127.0.0.1'
port = 9999
global address
address = (host,port)

#function for creating the socket for the client
def createSocket():
    try:
        global client
        client = socket.socket()
        client.connect(address)
        print('connected to '+address[0]+":"+str(address[1])+"...")
    except socket.error as msg:
            print('Error in creating or connecting: '+str(msg))
#function for chatting
#receives the message from the server
#asks the user for replay
#sends the replay to the server
def socketChat():
    try:
        while True:
            msg = str(client.recv(2048),'utf-8')
            print('Server: '+str(msg))
            replay = input('Client(You): ')
            if replay=="quit":
                break
            client.send(str.encode(replay))
    except socket.error as msg:
        print('Error in chatting: '+str(msg))

try:
    if __name__ == "__main__":
        createSocket()
        socketChat()
except KeyboardInterrupt:
    print("User interruption!\n")
