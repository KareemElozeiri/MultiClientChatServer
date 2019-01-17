import socket
import time
import threading
from queue import Queue

num_of_threads = 2
job_num = [1,2]
host = '127.0.01'
port = 9999
queue = Queue()
global address
address = (host,port)
global server
server = socket.socket()
#the list where the ip addressed of clients are stored
global all_addresses
all_addresses = []
#the list where the connection objects of the clients are stored
global all_connections
all_connections = []

#__thread one start___

#function to create the server and bind it to the address 127.0.0.1:9999
#and make it listen for connections
def createServer():
    try:
        print('server established..')
        server.bind(address)
        print('server is binded to '+address[0]+":"+str(address[1]))
        server.listen(5)
        print("server is listening for clients...")
    except socket.error as msg:
        print("Error in creating: "+str(msg))
        time.sleep(1)
        createServer()

#function to  make the server accept connections from the clients
#and add there addresses to the all_addresses list and add there
#connections to the all_connections list
def connectClient():
    #closing old connections
    for conn in all_connections:
        conn.close()
    #cleaning old addresses and connections
    del all_addresses[:]
    del all_connections[:]

    while True:
        try:
            #accepting connection from a client
            connection ,address = server.accept()
            #setting timeout to be none
            server.setblocking(1)
            #saving the address and connection object of the client
            all_addresses.append(address)
            all_connections.append(connection)
            print("Connection established with: "+address[0]+":"+str(address[1]))
        except socket.error as msg:
            print("Error in connecting with client: "+str(msg))
#__thread one end __

#__thread two start__

#function to create a shell interface for the user to see the connected client from
#it and to connect to any client
def prompot():
    print("CHAT SERVER version .1 ...")
    try:
        while True:
            command = input("CHAT>> ")
            #command to be entered to list available connections
            if command == 'ls':
                list_connections()
            #command to connect to a specific client
            elif 'select ' in command:
                connectToClient(command)
            else:
                print("Invalid command")
    except:
        print("Error in interacting with the shell!")
        time.sleep(1)
        prompot()

#function to list availavle coonnections
def list_connections():
    result = '__Availbale chats__\n'
    for i,connection in enumerate(all_connections):

        result += str(i)+"-"+str(all_addresses[i][0])+":"+str(all_addresses[i][1])+"\n"

    print(result)

#function to choose a specific client and start a chat with it
def connectToClient(command):
    #cleaning the command to get only the number of the target
    target = command.replace('select ','')
    try:
        #converting the target variable from string to integer
        target = int(target)
        try:
            #getting the connection
            client_conn = all_connections[target]
            client_addr = all_addresses[target]
            print("To quit type \q quit")
            while True:
                try:
                    #getting message from the server
                    message = input("Server(You): ")
                    #checking if the server want to quit the chat
                    if message=="\q quit":
                        prompot()
                    #sending the message to the client
                    client_conn.send(str.encode(message))
                    #reveiving the replay from the client
                    replay = str(client_conn.recv(20480),'utf-8')
                    print("Client("+client_addr[0]+":"+str(client_addr[1])+"): "+replay)
                except KeyboardInterrupt:
                    break
                except socket.error as msg:
                    print("Sokcet error: "+str(msg))

        except:
            print("Client not found!")

    except ValueError:
        print("Invalid input : enter the client number")
#__thread two end__


def create_threads():
    for n in range(num_of_threads):
        #creating threads with job is the function work
        t = threading.Thread(target=work)
        #stoping the tread after it has done its job
        t.daemon = True
        #starting the thread
        t.start()

def work():
    while True:
        job = queue.get()
        if job ==1:
            createServer()
            connectClient()
        if job ==2:
            prompot()
        queue.task_done()

def create_jobs():
    for job in job_num:
        queue.put(job)
    queue.join()


try:
    if __name__ == "__main__":
        create_threads()
        create_jobs()
except KeyboardInterrupt:
    print("User ended the operation")
