import requests
import yaml
import time
from urllib.parse import urlparse

# Gets path of YAML file of endpoints from user, load and read it
file_path = input("Enter the file path: ")
with open(file_path, 'r') as file:
    endpoints = yaml.load(file, Loader=yaml.FullLoader)

# Initializes avail map for up and total count for each domain listed in YAML file
avail={}
for endpoint in endpoints:
    domain = urlparse(endpoint['url']).netloc
    avail[domain] = {'up': 0, 'total': 0}

# Creates a dictionary for methods
method_dict = {"GET":requests.get, "POST":requests.post, "PUT":requests.put, "DELETE":requests.delete, "PATCH": requests.patch, "HEAD":requests.head, "OPTIONS":requests.options}

# Sends request to url via specified method with proper parameters, calculates latency and returns boolean value based on UP and DOWN results
def send_request(url, header, payload, method):
    latency=0
    start=0
    end = 0
    start = time.time()
    response = method_dict[method](url, headers=header, data=data)
    end = time.time()
    latency = end-start
    if response.status_code > 199 and response.status_code < 300 and latency < 0.5:
        return True
    else:
        return False

# Runs infinitely with 15 second intervals, calls send_request for each endpoint and prints availability rate of each domain
while 1:
    for endpoint in endpoints:
        url = ""
        header={}
        data={}
        method="GET"
        if 'url' in endpoint:
            url = endpoint['url']
        if 'headers' in endpoint:
            header = endpoint['headers']
        if 'body' in endpoint:
            data= endpoint['body']
        if 'method' in endpoint:
            method = endpoint['method']
        domain = urlparse(url).netloc
        result = send_request(url, header, data, method)
        if result:
            avail[domain]['up']+=1
        avail[domain]['total']+=1
        
    for domain in avail:
        avail_rate = 100*avail[domain]['up']/avail[domain]['total']
        print(f"{domain} has {avail_rate} availability rate")

    time.sleep(15)        