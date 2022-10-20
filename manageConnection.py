import time, requests, smtplib, ssl
import rmsApiReq #import module for functions to get device state and mobile ip

def url_chk(url, location):
    try:
        print('Checking device for valid connection: '+url+' ['+location+']')
        response = requests.get(url, timeout=5, headers={'Connection':'close'})
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        print('Device in use or offline. Please wait...')
        print(err)
        print('end of url check')
        return 0

