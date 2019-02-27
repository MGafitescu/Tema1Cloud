from http.server import BaseHTTPRequestHandler
import socketserver
import requests
import json
import random
from urllib.parse import urlparse, parse_qs
import logging
import re

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s %(message)s')
f = open("config.json")
config = json.load(f)
f.close()


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        parsed_url = urlparse(self.path)
        self.send_response(200)
        # Send headers

        if parsed_url.query != "":
            arguments = parse_qs(parsed_url.query)
            latitude = float(arguments["lat"][0])
            longitude = float(arguments["lon"][0])
        else:
            longitude = random.uniform(-90, 90)
            latitude = random.uniform(-90, 90)
        if parsed_url.path == "/geolocation":
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Send message back to client
            message = geolocation(latitude, longitude)
            json_string = json.dumps(message)
            self.wfile.write(bytes(json_string, "utf-8"))
        elif parsed_url.path == "/weather":
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Send message back to client
            message = weather_message(latitude, longitude)
            json_string = json.dumps(message)
            self.wfile.write(bytes(json_string, "utf-8"))
        elif parsed_url.path == "/pastebin":
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            message = pastebin(latitude, longitude)
            json_string = json.dumps(message)
            self.wfile.write(bytes(json_string, "utf-8"))
        elif parsed_url.path == "/metrics":
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            message = metrics()
            json_string = json.dumps(message)
            self.wfile.write(bytes(json_string, "utf-8"))
        else:
            self.send_header('Content-type', 'text')
            self.end_headers()
            message = "Non-existan"
            self.wfile.write(bytes(message, "utf-8"))

        return


def geolocation(latitude, longitude):
    geo_response = reverse_geocoding(latitude, longitude)
    message = dict()
    if len(geo_response["results"]) != 0:
        message["latitude"] = geo_response["results"][0]["annotations"]["DMS"]["lat"]
        message["longitude"] = geo_response["results"][0]["annotations"]["DMS"]["lng"]
        message["map"] = geo_response["results"][0]["annotations"]["OSM"]["url"]
        message["timezone"] = geo_response["results"][0]["annotations"]["timezone"]["name"]
        message["address"] = geo_response["results"][0]["formatted"]
    else:
        message["latitude"] = latitude
        message["longitude"] = longitude
        message["map"] = "No data found for these coordinates"
        message["timezone"] = "No data found for these coordinates"
        message["address"] = "No data found for these coordinates"
    return message


def reverse_geocoding(latitude, longitude):
    apiKey = config["geoApiKey"]
    url = "https://api.opencagedata.com/geocode/v1/json?q={}+{}&key={}".format(latitude, longitude, apiKey)
    payload = {}
    headers = {}
    response = requests.request('GET', url, headers=headers, data=payload, allow_redirects=False)
    logging.info("service:GEOCODING method:%s url:%s status:%s latency:%s response:%s\n", "GET", url,
                 response.status_code
                 , response.elapsed.total_seconds(), response.text.replace("\n", ""))
    return response.json()


def weather(latitude, longitude):
    apiKey = config["weatherApiKey"]
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&APPID={}".format(latitude,
                                                                                                      longitude, apiKey)
    payload = {}
    headers = {}
    response = requests.request('GET', url, headers=headers, data=payload, allow_redirects=False)
    logging.info("service:WEATHER method:%s url:%s status:%s latency:%s response:%s\n", "GET", url,
                 response.status_code, response.elapsed.total_seconds(), response.text.replace("\n", ""))
    return response.json()


def weather_message(latitude, longitude):
    response = weather(latitude, longitude)
    message = dict()
    message["main"] = response["weather"][0]["main"]
    message["description"] = response["weather"][0]["description"]
    message["temp"] = response["main"]["temp"]
    message["pressure"] = response["main"]["pressure"]
    message["humidity"] = response["main"]["humidity"]
    message["windspeed"] = response["wind"]["speed"]
    message["latitude"] = response["coord"]["lat"]
    message["longitude"] = response["coord"]["lon"]
    return message


def pastebin(latitude, longitude):
    apiKey = config["pasteBinApiKey"]
    url = 'https://pastebin.com/api/api_post.php'
    payload = {}
    location = geolocation(latitude, longitude)
    weather = weather_message(latitude, longitude)
    message = "Date despre locatie: \n"
    for (key, value) in location.items():
        message = message + "{}: {}\n".format(key, value)
    message = message + "\nDate despre vreme:\n"
    for (key, value) in weather.items():
        message = message + "{}: {}\n".format(key, value)
    payload["api_dev_key"] = apiKey
    payload["api_option"] = "paste"
    payload["api_paste_code"] = message
    headers = {}
    response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)
    logging.info("service:PASTEBIN method:%s url:%s status:%s latency:%s response:%s\n", "POST", url,
                 response.status_code, response.elapsed.total_seconds(), response.text.replace("\n", ""))
    pastebin_response = {}
    pastebin_response["message"] = message
    pastebin_response["link"] = response.text
    return pastebin_response


def metrics():
    f = open("example.log", "r")
    text = f.read()
    f.close()
    content = []
    content.append(re.findall("GEOCODING(.+)", text))
    content.append(re.findall("WEATHER(.+)", text))
    content.append(re.findall("PASTEBIN(.+)", text))
    status_codes = [[], [], []]
    latencies = [[], [], []]
    names = ["Reverse geocoding", "Weather", "Pastebin"]
    urls = ["https://opencagedata.com/api", "https://openweathermap.org/api", "https://pastebin.com/api"]
    for i in range(0, 3):
        for item in content[i]:
            status_codes[i].append(re.search("status:(\d+)", item).group(1))
            latencies[i].append(float(re.search("latency:(\d+\.\d+)", item).group(1)))

    status_codes_dicts = [{}, {}, {}]
    for i in range(0, 3):
        for items in status_codes[i]:
            status_codes_dicts[i][items] = status_codes[i].count(items)

    average_latencies = [sum(l) / len(l) for l in latencies]
    max_latencies = [max(l) for l in latencies]
    min_latencies = [min(l) for l in latencies]

    response = [{}, {}, {}]

    for i in range(0, 3):
        response[i] = dict()
        response[i]["nume"] = names[i]
        response[i]["url"] = urls[i]
        response[i]["apeluri"] = len(content[i])
        response[i]["status"] = status_codes_dicts[i]
        response[i]["latenta_avg"] = average_latencies[i]
        response[i]["latenta_max"] = max_latencies[i]
        response[i]["latenta_min"] = min_latencies[i]

    return response


def run():
    server_address = ('127.0.0.1', 8081)
    httpd = socketserver.ThreadingTCPServer(server_address, testHTTPServer_RequestHandler)
    httpd.serve_forever()


run()
