#CreamT
#periodically test for a valid connection

import time, requests, smtplib, ssl
import rmsApiReq #import module for functions to get device state and mobile ip

#functions
def url_chk(url):
    try:
        response = requests.get(url, timeout=5, headers={'Connection':'close'})
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        print(err)
        return 0

def send_mail(message):
    #SMTP settings
    portSSL = 465
    smtp_server = 'smtp.gmail.com'
    sender = 'creamtcam@gmail.com'
    reciever = 'peter.arber@plymouth.ac.uk'
    pwd = 'Vymvav-kikveb-2dexju'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, portSSL, context=context) as server:
        server.login(sender, pwd)
        server.sendmail(sender, reciever, message)
        server.quit()

deviceID = 273746 #ID of individual RUT device
location = 'DW'
#deviceID = 354389
#location = 'PZ'

portCT = 8080 #CreamT controller access port

rutIsOnline = False
deviceIsOnline = False

while(1):
    rutIsOnline = rmsApiReq.get_dev_status(deviceID)
    ipAddr = rmsApiReq.get_mobile_ip(deviceID)
    print(time.ctime())
    #url = 'http://' + ipAddr
    #response = url_chk(url)
    #check that the RUT modem is available
    #if response:
     #   print(response.ok)
      #  if response.text.find('URL=/cgi-bin/luci') > 0:
       #     print('RUT device OK')
        #    rutIsOnline = True
        #else:
         #   print("RUT device FAIL")
          #  rutIsOnline = False
    if rutIsOnline:
        print('RUT device OK')
    else:
        print("RUT device FAIL")
        #rutIsOnline = False

    if rutIsOnline:
        url = 'http://' + ipAddr + ':' + str(portCT) + '/CreamT/'
        response = url_chk(url)
        if response:
            #if not deviceIsOnline:
                #send_mail('Subject: CREAMT_MONITOR_DW \n\nDevice ONLINE')
            deviceIsOnline = True
            print('Device ONLINE')
        else:
            #if deviceIsOnline:
                #send_mail('Subject: CREAMT_MONITOR_DW \n\nDevice OFFLINE')
            deviceIsOnline = False
            #reboot device - after n reconnect attempts
            #requests.get('http://' + ipAddr + '/cgi-bin/output?username=CREAMT_DO_'+location+'&password=Coastal88&action=on&pin=oc&time=2')
            print('Device OFFLINE')
            time.sleep(10)
    break
    #time.sleep(600) #periodic check [seconds]
print('-----------------------------------')
print("")
print("Press enter to exit")
input()
