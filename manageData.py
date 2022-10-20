import time, os, math, requests, re, glob
import deviceInfo

def list_files_local(basepath):
    files = os.listdir(basepath)
    filenames = []
    filesizes = []
    for f in files:
        if f.endswith('.dat'):
            #print(f)
            filenames.append(f)
            s = os.stat(os.path.join(basepath,f))
            #print(s.st_size)
            filesizes.append(round(s.st_size/1000))
    return(filenames, filesizes)

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
    return(filenames, filesizes)

#compare lists of device files and local files and output list of new files that need to be downloaded
def list_new_scans(deviceNames, deviceSizes, localNames, localSizes, location):
    dlFiles = []
    localNames = [sub.replace('_'+location,'') for sub in localNames]
    for ix, i in enumerate(deviceNames):
        if i in localNames:
            for jx, j in enumerate(localNames):
                if i == j:       
                    #print(ix, i, deviceSizes[ix], jx, j, localSizes[jx])
                    if(abs(deviceSizes[ix] - localSizes[jx]) > 2):
                        dlFiles.append(i)
        else:
            dlFiles.append(i)
    return(dlFiles)

def get_scan_data(url, location, filename, basepath):
    print('Downloading file [{}]\r\nPlease wait...'.format(filename))
    try:
        response = requests.get(url + filename, headers={'Connection':'keep-alive'})
    except requests.exceptions.RequestException as err:
        print(err)
        return(-1)
    
    [name, ext] = os.path.splitext(filename)
    filepath = os.path.join(basepath, name + '_' + location + ext)
    #print(filepath)
    if response:
        #print(response)
        open(filepath, 'wb').write(response.content)
    else:
        print('No response from server!')
        return(-1)
    print('{} download completed! [{}]'.format(filename, int(os.path.getsize(filepath)/1000) )) 
    return(0)

def split_file(basepath, location, localNames, localSizes):
    #check log file for monthly files that are larger than the previous split
    #split new daily files from monthly data file
    logfile = 'scanLog_' + location + '.txt'
    logpath = os.path.join(basepath, logfile)
    logInfo = get_log_info(logpath)
    for jx, j in enumerate(localNames):
        if '_data' in j and '.dat' in j:
            if len(logInfo) == 0:
                #[date, time, filename, filesize]
                logInfo = [[0,0,j, localSizes[jx]]]
                parse_daily_scan(os.path.join(basepath, j), location)
            else:
                for ix, i in enumerate(logInfo):
                    #print(ix, i, j, localSizes[jx])
                    if j == i[2]:
                        if abs(int(i[3]) - int(localSizes[jx])) <= 2:
                            break
                        else:
                            logInfo[ix] = [0,0,j, localSizes[jx]]
                            parse_daily_scan(os.path.join(basepath, j), location)
                            break
                    else:
                        if ix >= len(logInfo)-1:     
                            logInfo.append([0,0,j, localSizes[jx]])
                            parse_daily_scan(os.path.join(basepath, j), location)
    #print(logInfo)
    #write updated log file
    write_log_info(logpath, logInfo)
    return(0)

def get_log_info(logfile):
    #get list of previous saved data from log
    l = open(logfile,"a+")
    l.seek(0,0)
    logInfo = list()
    while 1:
        temp = l.readline()
        #print(temp)
        if len(temp) == 0:
            break   
        if len(temp) > 1:
            y = re.split("\s", temp)
            logInfo.append(y)
    l.close()
    return(logInfo)

def write_log_info(logfile, logInfo):
    #write current saved data to log
    tm_obj = time.gmtime(time.time())
    l = open(logfile,"w+")
    for i in logInfo:
        l.write("%02d/%02d/%02d %02d:%02d:%02d %s %s\r\n" % (tm_obj.tm_mday, tm_obj.tm_mon, tm_obj.tm_year-2000,  tm_obj.tm_hour, tm_obj.tm_min, tm_obj.tm_sec, i[2], i[3]))
    l.close()
    return(0)



def parse_daily_scan(filepath, location):
    basepath = os.path.split(filepath)
    basepath = basepath[0]
    scanpath = os.path.join(basepath, 'SCAN_DATA')
    if not os.path.isdir(scanpath):
        os.mkdir(scanpath)
    #open monthly file
    f = open(filepath, 'r')
    header = f.readline()
    #extract daily scan data and save to file
    last = ''
    while(1):
        #read monthly data
        data = f.readline()
        #check for EoF
        if len(data) == 0:
            break
        #get scan timestamp
        x = re.split("\s", data)
        timestamp = int(x[0])
        del x
        tm_obj = time.gmtime(timestamp)
        filename = "%2d%02d%02d_All_SCANS_%s.dat" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday, location)
        filepath = os.path.join(scanpath, filename)
        if filename != last:
            last = filename
            #print(filepath)
            with open(filepath,'w') as s:
                s.write(header)
        else:
            with open(filepath, 'a') as s:
                s.write(data)
    f.close()
    s.close()


    def split2():

####Opens daily file and reads data####
        m = open(filepath, 'r')
        header = m.readline()
        m.close
        
    ##### Opens files and splits to get timestamp #####
        time_list1=[]
        with open(filepath, 'r') as f:
            for line in f:
                line = line.split()
                line = line[0]
                time_list1.append(line)
        del time_list1[0]
        time_list2 = [int(i) for i in time_list1]
        f.close
        llen = int(len(time_list2))
        
        
        with open(filepath) as f:
            data = f.readlines()
            
        ilist=[]
        count = 1 
        ###Loops through list looking for 2 second gap or larger ####
        for i, value in enumerate(time_list2): 
            if value > time_list2[i-1]+3:
                count = count +1
                scount = str(count) +'_'
                i+= 1 
                int(i)
                ilist.append(i)
                #print(i, value, count,scount)
                print(ilist)

                filename1 = "%2d%02d%02d_SCAN_%s%s.dat" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday, scount, location)
                filename2 = "%2d%02d%02d_SCAN_1_%s.dat" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday, location)
                filepath1 = os.path.join(scanpath, filename1)
                filepath3 = os.path.join(scanpath, filename2)

        ####writes new time scan files with correct start points, but not end  #####      
                for x in ilist:
                    with open(filepath1, 'w') as f:
                        f.write(header)
                        f.write(''.join(data[i:llen+1]))
                        f.close() 
                        #print('file written')

        #### File paths for if there is no 3 second gap #####                

        filename2 = "%2d%02d%02d_SCAN_1_%s.dat" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday, location)
        filepath3 = os.path.join(scanpath, filename2)                

        #### writes 1st time scan file #####
        with open(filepath3, 'w') as f:
            if bool(ilist) == False:
                f.write(''.join(data))
                f.close() 
            else:
                f.write(''.join(data[0:ilist[0]]))
                f.close() 
        
        ##creates new files list ####

        globpath = filepath + "\\_SCAN_DATA"
        timestr = str("%2d%02d%02d" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday))
        scan = "_SCAN_"
        filelist = glob.glob(globpath + timestr + scan + "*.dat")
        print(filelist)

        #### Function for deleting unwanted data from files, so files are per scan. ######

        def split3(filelist):
            print("Split 3 starting")
            print(filelist)
            for newfile in filelist:
                newfile = str(newfile)
                #print(newfile)

                ilist2 =[]
                time_list3 = []
                count1 = 0
                
                ##### gets timestamps from files ####
                with open(newfile, 'r') as f:
                    next(f)  ###skips header ###
                    for line1 in f:
                        line1 = line1.split()
                        line1 = line1[0]
                        time_list3.append(line1)
                        time_list3 = [int(i) for i in time_list3]
                                
                ###### Loops through for 3 second gap or greater#####
                for i1, value in enumerate(time_list3): 
                    if value > time_list3[i1-1]+2:
                        count1 = count1 +1 
                        scount = str(count1)
                        i1 += 1 
                        int(i1)
                        ilist2.append(i)
                        #print(i1, value, count1 )
                        break
                                
                f.close()
                
                #### Opens data to be written #####
                with open(newfile, 'r') as f:
                    data1 = f.readlines()
                    f.close()
                
                #### Writes data from 3 second gap to end, or from start to 2 second gap ######
                with open(newfile, 'w') as f:
                    if i1 < 1:
                        f.write(''.join(data1[i1:]))
                    else:
                        f.write(''.join(data1[0:i1]))
                        f.close

    
                
              
        split3(filelist)
    split2()
   
    return(0)
