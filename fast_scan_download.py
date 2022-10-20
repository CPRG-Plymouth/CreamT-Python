from fileinput import filename
import requests, time
import rmsApiReq

##### This script is not finished #######

IP = input("Please Enter Device IP: ")
port = 8080


def build_url(IP, port):
    url = 'http://' + str(IP) + ':' + str(port) + '/CreamT/'
    return(url)


def http_get(url):
    try:
        response = requests.get(url, timeout=5, headers={'Connection':'close'})
        response.raise_for_status()
        return(response.text)
    except requests.exceptions.RequestException as err:
        print(err)
        return(0)


def list_files_device(response):
    response = str(response)
    eof = 0
    ind = 0
    i = 0
    filenames = []
    filesizes = []
    while(not eof):
        ind = response.find('data.dat</td>', ind+1)
        if(ind <= 0):
            eof = 1
            break
        #filename
        indStart = response.find('<td>', ind-12)+4
        indEnd   = response.find('</td>', ind)
        filenames.append(response[indStart:indEnd])
        #size
        indStart = response.find('<td style="text-align:right;">', ind)+30
        indEnd   = response.find('</td>', indStart)
        filesizes.append(int(response[indStart:indEnd]))
        i += 1
    print(filenames, filesizes)
    return(filenames, filesizes)
        


url = build_url(IP, port)
response = http_get(url)
list_files_device(response)

