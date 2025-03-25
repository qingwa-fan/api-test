import http.server
import socketserver
import os
from functools import partial
import sys

class HttpServer:
    def __init__(self, bind="127.0.0.1", port=9987, directory=os.getcwd()):
        self.bind = bind
        self.port = port
        self.directory = directory
        args = sys.argv
        for i in range(1, len(args)):
            if args[i] == "-port" and i + 1 < len(args):
                self.port = int(args[i + 1])
            if args[i] == "-dir" and i + 1 < len(args):
                self.directory = args[i + 1]
            if args[i] == "-bind" and i + 1 < len(args):
                self.bind = args[i + 1]

    def run(self):
        try:
            with socketserver.TCPServer((self.bind, self.port), partial(http.server.SimpleHTTPRequestHandler, directory=self.directory)) as httpd:
                print(f"工作目录: {self.directory}\nServing HTTP on {self.bind} port {self.port}\nhttp://{self.bind}:{self.port}/")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

if __name__ == '__main__':
    server = HttpServer()
    server.run()
