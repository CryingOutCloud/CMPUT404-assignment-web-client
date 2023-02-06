#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split(" ")[1]
        return int(code)

    def get_headers(self,data):
        headers = data.split("\r\n\r\n")[0] + "\r\n\r\n"
        return headers

    def get_body(self, data):
        parts = data.split("\r\n\r\n")
        if len(parts) > 1:
            return parts[1]
        else:
            return ""
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # Construct the GET path from theurl componenets
    def generate_path(self, url_parts):
        path = url_parts.path
        if not path:
            path = "/"
        if url_parts.query:
            path += f"?{url_parts.query}"
        return path

    def GET(self, url, args=None):

        url_parts = urlparse(url)
        path = self.generate_path(url_parts)
        self.connect(url_parts.hostname, url_parts.port)

        self.sendall(
            f"GET {path} HTTP/1.1\r\n" +
            f"Host:{url_parts.hostname}\r\n\r\n"
        )
        
        data = self.socket.recv(4096)

        print("\ndata: ", data)

        code = self.get_code(str(data))
        body = self.get_body(str(data))

        print("\ncode: ", code)
        print("\nbody: ", body)

        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
