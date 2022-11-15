import time, os, math, requests, re

def parse_daily_scan():
    #open monthly file
    f = open('2207_data.dat', 'r')
    header = f.readline()
    #print(header)
    #extract daily scan data and save to file
    last = ''
    
    while(1):
        
        #read monthly data
        data = f.readline()
        #print(data)
        #check for EoF
        if len(data) == 0:
            break
        #get scan timestamp
        x = re.split("\s", data)
        timestamp = int(x[0])
        del x
        ###splits data by by UTC #####
        tm_obj = time.gmtime(timestamp)
        #print(tm_obj)
        filename = "%2d%02d%02d_SCAN_%s.dat" % (tm_obj.tm_year-2000, tm_obj.tm_mon, tm_obj.tm_mday, 'HGI')
        filepath = r'C:\Users\msymons2\OneDrive - University of Plymouth\Cream T\CreamT Python\2207_data_new.dat'


        #####writes just the header if its a new day #####
        if filename != last:
            last = filename
            #print(filepath)
            with open(filepath,'w') as s:
                s.write(header)
        
        ####writes the data to the file based on the time objects based on UTC time ######
        else:
            #print(filepath)
           with open(filepath, 'a') as s:
                s.write(data)

        with open(filepath, 'r') as n:
            new = n.readlines()
            print(new[10:])
            
            
        
        
    f.close()
    s.close()
    
   
   
    
   
parse_daily_scan()