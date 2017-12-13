# server.py
 
import sys
import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 9020)
sock.bind(server_address)
sock.listen(10)
cname = "unknown"
name = "aaron"



 
print "Chat server started on port 9020"
 
while 1:
    conn, client_ip = sock.accept()
    try:
        print "client connected" + str(client_ip)
        welcome  = "Welcome to " + name + "'s chat room\r\n"
        conn.sendall(welcome)
        chat_buff = ""
        while 1:
            data = conn.recv(4096)
            if data[-2:] != "\r\n":
                data = data + conn.recv(4096)
            print data
            chat = data.split('\r\n')

            
            for switch in chat:
                if switch == "":
                    continue
                elif switch == "help":
                    conn.sendall("here are your available commands:\n    help -shows this help list\n    test: <words> -shows a test of the chat you might want to send\n     name: <chatname> -specifies your name\n    get -receive a response with the contents of chat server\n    push: <stuff> -receives a response of OK<cr><lf> The result is that <chatname>: <stuff> is added as a new line to the chat\n     getrange <startline> <endline> -receives a response of lines <startline> through <endline> from the chat buffer. getrange assumes a 0-based buffer. Your client should return lines <startline> <endline>\n    adios -will end current session\r\n")
                elif switch == "get":
                    conn.sendall(chat_buff + "\r\n")
                elif 0 <= 4 < len(switch) and switch[4] == ":":
                    if switch[:4] == "name":
                        cname = switch[6:]
                        conn.sendall("OK\r\n")
                    elif switch[:4] == "push":
                        chat_buff += cname + ": " + switch[6:] + "\n"
                        conn.sendall("OK\r\n")
                    elif switch[:4] == "test":
                        conn.sendall(switch[6:] + "\r\n")
                elif switch == "adios":
                    conn.sendall("adios\r\n")
                elif switch[:9] == "getrange ":
                    text = ""
                    range = switch.split()
                    try:
                        rangestart = int(range[1])
                        rangeend = int(range[2])
                        chat = chat_buff.split('\n')
                        while(rangestart <= rangeend):                            
                            text = text + chat[rangestart] + "\n"
                            rangestart = rangestart + 1
                    except IndexError:
                        text = "youre index was out of range or you didnt enter in both args"
                    finally:
                        conn.sendall(text + "\r\n")
                elif switch == "who is the coolest":
                    conn.sendall("aaron duh\r\n")
                elif switch != "get" or switch[:5] != "name:" or switch[:5] != "push:" or switch[:5] != "test:" or  switch[:9] != "getrange " or switch != "adios" or switch != "help":
                    conn.sendall("unrecognized command " + switch + "\r\n")



    finally:
        conn.close()

