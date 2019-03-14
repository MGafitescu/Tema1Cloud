from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import re
import services


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def send(self, response, content, content_type):
        self.send_response(response)
        self.send_header('Content-type', content_type)
        self.end_headers()

        self.wfile.write(bytes(content, "utf-8"))

    # GET
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path.startswith("/periods"):
            try:
                response, content, content_type = periods_get_controller(parsed_url.path)
            except Exception as e:
                print(e)
                response, content, content_type = (500, "Internal server error", "text/html")
        elif parsed_url.path.startswith("/types"):
            try:
                response, content, content_type = types_get_controller(parsed_url.path)
            except Exception as e:
                print(e)
                response, content, content_type = (500, "Internal server error", "text/html")
        else:
            response, content, content_type = (400, "Bad route", "text/html")

        self.send(response, content, content_type)

        return

    def do_POST(self):
        response, content, content_type = (400, "Bad route", "text/html")
        parsed_url = urlparse(self.path)
        rec_content_type = self.headers["content-type"]
        content_length = int(self.headers["content-length"])
        rec_content = self.rfile.read(content_length)
        if rec_content_type != "application/json":
            response, content, content_type = (415, "Content type should be application/json", "text/html")
            self.send(response, content, content_type)
            return
        elif content_length == 0:
            response, content, content_type = (400, "Request should not be empty", "text/html")
            self.send(response, content, content_type)
            return
        else:
            try:
                payload = json.loads(rec_content)
            except ValueError:
                response, content, content_type = (415, "Content is not a valid json", "text/html")
                self.send(response, content, content_type)
                return
            if parsed_url.path.startswith("/periods"):
                try:
                    response, content, content_type = periods_post_controller(parsed_url.path, payload)
                except Exception as e:
                    print(e)
                    response, content, content_type = (500, "Internal server error", "text/html")

        self.send(response, content, content_type)
        return

    def do_PUT(self):
        response, content, content_type = (400, "Bad route", "text/html")
        parsed_url = urlparse(self.path)
        rec_content_type = self.headers["content-type"]
        content_length = int(self.headers["content-length"])
        rec_content = self.rfile.read(content_length)
        if rec_content_type != "application/json":
            response, content, content_type = (415, "Content type should be application/json", "text/html")
            self.send(response, content, content_type)
            return
        elif content_length == 0:
            response, content, content_type = (400, "Request should not be empty", "text/html")
            self.send(response, content, content_type)
            return
        else:
            try:
                payload = json.loads(rec_content)
            except ValueError:
                response, content, content_type = (415, "Content is not a valid json", "text/html")
                self.send(response, content, content_type)
                return
            if parsed_url.path.startswith("/periods"):
                try:
                    response, content, content_type = periods_put_controller(parsed_url.path, payload)
                except Exception as e:
                    print(e)
                    response, content, content_type = (500, "Internal server error", "text/html")

        self.send(response, content, content_type)
        return

    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path.startswith("/periods"):
            try:
                response, content, content_type = periods_delete_controller(parsed_url.path)
            except Exception as e:
                print(e)
                response, content, content_type = (500, "Internal server error", "text/html")
        else:
            response, content, content_type = (400, "Bad route", "text/html")

        self.send(response, content, content_type)
        return


def periods_get_controller(path):
    response, content, content_type = (400, "Bad route", "text/html")
    if path == "/periods":
        response, content, content_type = services.get_periods()
    match = re.match(r"/periods/(\d+)$", path)
    if match is not None:
        id = match.group(1)
        response, content, content_type = services.get_period(id)
    return response, content, content_type


def periods_post_controller(path, payload):
    if path == "/periods":
        response, content, content_type = services.add_period(payload)
    else:
        response, content, content_type = (400, "Bad route", "text/html")
    return response, content, content_type


def periods_put_controller(path, payload):
    response, content, content_type = (400, "Bad route", "text/html")
    if path == "/periods":
        response, content, content_type = 405, "PUT not allowed on collection", "text/html"
    match = re.match(r"/periods/(\d+)", path)
    if match is not None:
        id = match.group(1)
        response, content, content_type = services.update_period(payload, id)
    return response, content, content_type


def periods_delete_controller(path):
    response, content, content_type = (400, "Bad route", "text/html")
    if path == "/periods":
        response, content, content_type = 405, "DELETE not allowed on collection", "text/html"
    match = re.match(r"/periods/(\d+)$", path)
    if match is not None:
        id = match.group(1)
        response, content, content_type = services.delete_period(id)
    return response, content, content_type

def types_get_controller(path):
    response, content, content_type = (400, "Bad route", "text/html")
    if path == "/types":
        response, content, content_type = services.get_types()
    match = re.match(r"/types/(\d+)$", path)
    if match is not None:
        id = match.group(1)
        response, content, content_type = services.get_type(id)
    return response, content, content_type


def run():
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print("Server started")
    httpd.serve_forever()


run()
