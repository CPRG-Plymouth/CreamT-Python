from this import s
import time, os, math, requests, re, glob
from datetime import date 
import deviceInfo


def split2():

    tdate = str(date.today())
    print(tdate)
    filepath = input("enter full file path: ")
    filedate = input("enter date of File in YYYY-MM-DD format:  ")
    location = input("enter site location: ")
    tm_obj = time.gmtime(time.time())
    basepath = 'K:\\Uni_Testing_FILES'
    scanpath = os.path.join(basepath, 'SCAN_DATA')
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
            scount = str(count) + '_'
            i+= 1 
            int(i)
            ilist.append(i)
            #print(i, value, count,scount)
            print(ilist)

            filename1 = "SCAN_"+ scount + location + "_" + filedate + ".dat" 
            filename2 = "SCAN_1_Uni_Testing_" + filedate + ".dat"
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

    filename2 = "SCAN_1_" + location + filedate + ".dat"
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
    filelist = glob.glob(r'K:\\Uni_Testing_FILES\SCAN_DATA\[SCAN]*.dat')
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