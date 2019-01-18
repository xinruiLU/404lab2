#!/usr/bin/env python3
import socket
import time

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

addr_info = socket.getaddrinfo("www.google.com", 80, proto=socket.SOL_TCP)
(family, socketype, proto, canonname, sockaddr) = addr_info[0]

def main():
    #create socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #allows to reuse same bind port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      

        s.bind((HOST, PORT))
        s.listen(1) #make socket listen
       
        #listen forever for connections
        while True:
            conn, addr = s.accept() #accept incoming connections
            with conn:
                #create a socket
                with socket.socket(family, socketype) as proxy_end:
                    #connect 
                    proxy_end.connect(sockaddr)
                    full_data = b""
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            break
                        full_data += data
                    proxy_end.sendall(full_data)
                    full_data_from_google = b""
                    while True:
                        data = proxy_end.recv(BUFFER_SIZE)
                        if not data:
                            break
                        full_data_from_google += data
                    conn.sendall(full_data_from_google)
            #print(full_data)
            #send data back as response
            time.sleep(0.5)
           # conn.sendall(full_data)
 

if __name__ == "__main__":
    main()

