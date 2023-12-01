import socket
import os
from termcolor import colored
import tqdm

class Server:


    def __init__(self, IP, port):

        self.IP = IP
        self.port = port

    def SetUP(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.IP, self.port))
        server.listen()

        print (f'{colored("[+]", "light_green")} Server is Running waiting for connections....')

        client, addr = server.accept()
        print (f'{colored("[*]", "blue")} Connection from: {addr}')

        file_name = client.recv(1024).decode()
        file_size = client.recv(1024)

        print (f'{colored("[*]", "blue")} file name will be {file_name}')
        print (f'{colored("[*]", "blue")} file size will be {file_size}')



        file = open(file_name, 'wb')
        file_byte = b""

        done = False
        progress = tqdm.tqdm(unit="B", unit_scale=True,unit_divisor=1000, total=int(file_size))

        while not done:
            data = client.recv(1024)
            if file_byte[-5:] == b'<END>':

                done = True
            else:
                file_byte += data

            progress.update(1024)

        file.write(file_byte)
        file.close()
        client.close()
        server.close()



class Client:

    def __init__(self, IP, port, file_path, file_name):

        self.IP = IP
        self.port = port
        self.file_path = file_path
        self.file_name = file_name

    def SetUP(self):
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.IP, self.port))

        file = open(self.file_path, 'rb')
        file_size = os.path.getsize(self.file_path)

        print (f'{colored("[*]", "blue")} file size {file_size}')

        client.send(self.file_name.encode())
        client.send(str(file_size).encode())

        data_content = file.read()
        client.sendall(data_content)
        client.send(b'<END>')
        
        file.close()
        client.close()



if __name__ == '__main__':

    print ("""
Server = 0
Client = 1
""")
    service = input('\nSet Service Do you want: ')


    if int(service) == 0:

        object = Server(IP=socket.gethostbyname(socket.gethostname()), port=8888).SetUP()

    elif int(service) == 1:

        file_name = input('Set file name with the extended: ')
        file_path = input('Set the file Path: ')

        object = Client(IP=socket.gethostbyname(socket.gethostname()), port=8888, file_name=file_name, file_path=file_path).SetUP()
