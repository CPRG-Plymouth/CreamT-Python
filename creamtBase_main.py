#monitor all deployed CreamT scanners
    #automatic data downloading to server
    #continual device monitoring and automatic resetting on crash

#python libraries
import os, time, requests, calendar
#CreamT libraries
import deviceInfo, rmsApiReq, manageConnection, manageData, googleAPI

basepath = 'K:\\'
#basepath = '/home/mark'

#connection information
port = 8080
retrys = 10
#class to hold device information
class Devices:
    ID = 0 #List of IDs of all CreamT scanner RUT devices
    location = ''
    IP =  ''
    time = '1970-01-01 00:00:00'
    tideNext = '1970-01-01 00:00:00'
    tideLast = '1970-01-01 00:00:00'
    isOnlineDEV = False
    devAttempt = 0
    isOnlineRUT = False
    rutAttempt = 0
    diff = 3600
    scanDl = True

#create device instance and assign device ID's.  Mark Symons - these are assigned for each rut - use rmsGetDeviceInfo.py to find ID number.
# Note DWL and PNZ will need to change due to bad open collectors on these Ruts

#s1 = Devices() #do this for every new device added
#s1.ID = 273746
#s1.location = 'DWL'

s2 = Devices()
s2.ID = 214262
s2.location = 'TorX'  

s3 = Devices()
s3.ID = 530346
s3.location = 'HGI'

dev = [s3,s2]

#start loop timer
starttime = time.time()
dltime = calendar.timegm(time.strptime(time.strftime('%d/%m/%y'),'%d/%m/%y'))
#print(dltime)
dlflag = True

while(1):
    #download new scans at 00:00 each day
    if time.time() >= dltime:
        #print(time.time(),dltime)
        dltime = calendar.timegm(time.strptime(time.strftime('%d/%m/%y'),'%d/%m/%y'))+86400
        for s in dev:
            s.scanDl = True
        #print(time.time(),dltime)

    for s in dev:
        if abs(s.diff) < 300:
            print('Scanning!')
            if isinstance(s.tideNext, str):
                s.diff = deviceInfo.time_diff(deviceInfo.to_seconds(s.tideNext))
            continue

        filepath = os.path.join(basepath, s.location + '_FILES')
        if not os.path.isdir(filepath):
            try:
                os.mkdir(filepath)
                dlflag = True
            except OSError as err:
                dlflag = False
                print(err)
                print('Cannot download data to specified file location, check the basepath exists')
        else:
            dlflag = True

        #check RUT status
        if not rmsApiReq.get_dev_status(s.ID):
            print("Rut status: \t\t[{}]" .format(0))
            if s.isOnlineRUT:
                s.isOnlineRUT = False
            s.rutAttempt += 1
            if s.rutAttempt >= 3:
                print('sending mail')
                googleAPI.rut_mail(s.ID, s.isOnlineRUT, s.location, s.IP)
                s.rutAttempt = 0
            continue
        else:
            if not s.isOnlineRUT:
                s.IP = rmsApiReq.get_mobile_ip(s.ID)
                s.isOnlineRUT = True
                googleAPI.rut_mail(s.ID, s.isOnlineRUT, s.location, s.IP)
            s.IP = rmsApiReq.get_mobile_ip(s.ID)


        if s.IP == 0:
            continue
        
        url = deviceInfo.build_url(s.IP, port)
        #check device is online - send an email if status changes
        if not manageConnection.url_chk(url, s.location):
            s.IP = rmsApiReq.get_mobile_ip(s.ID)
            if s.isOnlineDEV:
                if s.devAttempt < 0:
                    s.devAttempt = 0
                s.isOnlineDEV = False
            s.devAttempt += 1
            print(s.devAttempt)
            if s.devAttempt >= 6:
                s.devAttempt = -1
                print('resetting controller')
                print(s.IP)
                googleAPI.dev_mail(s.ID, s.isOnlineDEV, s.location, s.IP)
                try:
                    requests.get('http://' + s.IP + '/cgi-bin/output?username=CREAMT_DO&password=Coastal88&action=on&pin=4pin&time=2')
                except requests.exceptions.RequestException as err:
                    print('Device reset failed!')
                    print(err)
            continue
        else:
            if not s.isOnlineDEV:
                if s.devAttempt < 0:
                    s.isOnlineDEV = True
                    googleAPI.dev_mail(s.ID, s.isOnlineDEV, s.location, s.IP)
                s.devAttempt = 0
        
        #get current device values 
        s.time = deviceInfo.get_value(url, '?Tval')
        tideTemp = deviceInfo.get_value(url, '?TIDE')

        if tideTemp != s.tideNext:
            s.tideLast = s.tideNext
            s.tideNext = tideTemp

        if isinstance(s.tideNext, str):
            s.diff = deviceInfo.time_diff(deviceInfo.to_seconds(s.tideNext))

        if s.diff > 3600 and s.scanDl and dlflag:
            print(s.location + ': Checking scans...')
            [locNames, locSizes] = manageData.list_files_local(filepath)
            [devNames, devSizes] = manageData.list_files_device(deviceInfo.http_get(url + '?FILE'))
            dlFiles = manageData.list_new_scans(devNames, devSizes, locNames, locSizes, s.location)
            if len(dlFiles):
                for i in dlFiles:
                    a=0
                    manageData.get_scan_data(url, s.location, i, filepath)
            [locNames, locSizes] = manageData.list_files_local(filepath)
            manageData.split_file(filepath, s.location, locNames, locSizes)
            s.scanDl = False

        #print('Site\tRut Status\tMobile IP\t\tDevice Time\t\tLast Tide\t\tNext Tide [UTC]\t\tTime to Next Tide [s]')
        print('[{} | {} | {} | {} | {} | {} | {}]'.format(s.location,s.isOnlineRUT,s.IP,s.time,s.tideLast,s.tideNext,s.diff))

    #time.sleep(5)   
    time.sleep(600 - time.time() % 600)
    #time.sleep(600)