import requests
import yaml
import time
from urllib.parse import urlparse

#Defining params to use in program  
url = ""
header={}
data={}
avail ={}
latency=0
start=0
end = 0

# Gets path of YAML file of endpoints from user, load and read it
file_path = input("Enter the file path: ")
with open(file_path, 'r') as file:
    endpoints = yaml.load(file, Loader=yaml.FullLoader)
# Initializes avail map for up and total count for each domain listed in YAML file
for endpoint in endpoints:
    domain = urlparse(endpoint['url']).netloc
    avail[domain] = {'up': 0, 'total': 0}

# Sends request to url via specified method with proper parameters, calculates latency and returns boolean value based on UP and DOWN results
def send_request(url, header, payload, method):
    try:
        if method=="GET":
            start = time.time()
            response = requests.get(url, headers=header, data=data)
            end = time.time()
        elif method=="POST":
            start = time.time()
            response = requests.get(url, headers=header, data=data)
            end = time.time()
        elif method=="PUT":
            start = time.time()
            response = requests.put(url, headers=header, data=data)
            end = time.time()
        elif method=="DELETE":
            start = time.time()
            response = requests.delete(url, headers=header, data=data)
            end = time.time()
        elif method=="PATCH":
            start = time.time()
            response = requests.patch(url, headers=header, data=data)
            end = time.time()
        elif method=="HEAD":
            start = time.time()
            response = requests.head(url, headers=header, data=data)
            end = time.time()
        elif method=="OPTIONS":
            start = time.time()
            response = requests.options(url, headers=header, data=data)
            end = time.time()
        elif method=="CONNECT":
            start = time.time()
            response = requests.connect(url, headers=header, data=data)
            end = time.time()
        elif method=="TRACE":
            start = time.time()
            response = requests.trace(url, headers=header, data=data)
            end = time.time()

        latency = end-start
        if response.status_code > 199 and response.status_code < 300:
            if latency < 0.5:
                return True
            else:
                return False
        else:
            return False

    except:
        return False

# Runs infinitely with 15 second intervals, calls send_request for each endpoint and prints availability rate of each domain
while 1:
    for endpoint in endpoints:
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
