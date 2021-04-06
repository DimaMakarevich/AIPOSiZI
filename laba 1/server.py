from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import mimetypes
import os.path
import argument_parser


class S(BaseHTTPRequestHandler):
    local_path = []

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', mimetypes.guess_type(self.path[1::]))
        self.end_headers()

    def do_GET(self):
        if self.path != "/favicon.ico":
            if os.path.exists(self.path[1::]):
                self.send_response(200)
              #  self.send_header('Access-Control-Allow-Origin', "http://localhost:" + argument_parser['port'])
                self.send_header('Content-type', mimetypes.guess_type(self.path[1::]))
                self.end_headers()
                # self.log_message('"%s" %s ',self.requestline, str(200))
                # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
                self.local_path.append(self.path[1::])
                with open(self.local_path[0], "rb") as data:
                    f = data.read()
                    b = bytearray(f)
                    self.wfile.write(b)
                self.local_path.pop()
                with open("request.log", "a") as file:
                    log = "GET request /HTTP/1.1 200\nPath:\n{} \nHeaders:\n{}\n".format(self.path[1::],
                                                                                         self.headers)
                    file.write(log)
            else:
                self.send_response(500)
                # self.send_header('Content-type', mimetypes.guess_type(self.path[1::]))
                self.end_headers()
                with open("request.log", "a") as file:
                    log = "GET request /HTTP/1.1 200\nPath:\n{} \nHeaders:\n{}\n".format(self.path[1::],
                                                                                         self.headers)
                    file.write(log)

    def do_POST(self):
        if os.path.exists(self.path[1::]):
            self.send_response(200)
           # self.send_header('Access-Control-Allow-Origin', "http://localhost:" + argument_parser['port'])
            self.send_header('Content-type', mimetypes.guess_type(self.path[1::]))
            self.end_headers()
            with open(self.path[1::], "rb") as file:
                data = file.read()
            b = bytearray(data)
            with open("files/post/" + self.path[1::], 'wb') as file:
                file.write(b)
            with open("request.log", "a") as file:
                log = "POST request /HTTP/1.1 200\nPath:\n{} \nHeaders:\n{}\n".format(self.path[1::], self.headers)
                file.write(log)
        else:
            self.send_response(400)
            # self.send_header('Content-type', mimetypes.guess_type(self.path[1::]))
            self.end_headers()
            with open("request.log", "a") as file:
                log = "POST request /HTTP/1.1 400\nPath:\n{} \nHeaders:\n{}\n".format(self.path[1::], self.headers)
                file.write(log)

    def do_OPTIONS(self):
        self.send_response(200)
       # self.send_header('Access-Control-Allow-Origin', "http://localhost:" + argument_parser['port'])
        self.send_header('Access-Control-Allow-Methods', "POST, GET, OPTIONS")
        self.end_headers()
        with open("request.log", "a") as file:
            log = "OPTIONS request /HTTP/1.1 200 \nHeaders:\n{}\n".format(self.headers)
            file.write(log)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    argument_parser = argument_parser.parse_arguments()
    run(port=argument_parser['port'])