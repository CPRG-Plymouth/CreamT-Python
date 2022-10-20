import requests, time
import rmsApiReq

'''
#connection information
port = 8080
deviceID = 273746 #ID of individual RUT device

ipAddr = rmsApiReq.get_mobile_ip(deviceID)
url = 'http://' + ipAddr + ':' + str(portCT) + '/CreamT/'
'''
def build_url(ipAddr, port):
    url = 'http://' + str(ipAddr) + ':' + str(port) + '/CreamT/'
    return(url)

def http_get(url):
    try:
        response = requests.get(url, timeout=5, headers={'Connection':'close'})
        response.raise_for_status()
        return(response.text)
    except requests.exceptions.RequestException as err:
        print(err)
        return(0)

def to_seconds(timeStr):
    tmStruct = time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    timeSec = time.mktime(tmStruct)
    timeSec = int(timeSec)
    print(timeSec)
    return(timeSec)
    
def get_value(url, xhttpId):
    value = http_get(url+xhttpId)
    return(value)

def time_diff(timeSec):
    tmStruct = time.gmtime()
    now = time.mktime(tmStruct)
    now = int(now)
    #handle dst difference between system clock and device
    if tmStruct.tm_isdst:
        now = now-3600
    timeDiff = timeSec - now
    return(timeDiff)

#def is_last_tide(timeStr): #check if tide time is last of the day

'''
deviceTime = get_value('?Tval')
nextTide = get_value('?TIDE')

print(deviceTime)
print(nextTide)

print(time.asctime(time.localtime(to_seconds(deviceTime))))

print(time_diff(to_seconds(nextTide)))
print(time.asctime(time.localtime(abs(time_diff(to_seconds(nextTide))))))
'''
