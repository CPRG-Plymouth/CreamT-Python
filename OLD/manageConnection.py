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

def send_mail(message):
    #SMTP settings
    portSSL = 465
    smtp_server = 'smtp.gmail.com'
    sender = 'bscan.system@gmail.com'
    reciever = 'mark.symons@plymouth.ac.uk'
    pwd = 'BSCAN2022'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, portSSL, timeout=120) as server:
        server.login(sender, pwd)
        server.sendmail(sender, reciever, message)
        server.quit()

def rut_mail(id, status, location):
    #message on change of rut status
    subject = 'Subject: CREAMT_MONITOR_' + location
    if status:
        body = 'RUT Device: ID [{}] \nONLINE'.format(id)
    else:
        body = 'RUT Device: ID [{}] \nOFFLINE\n\nResetting: If an online e-mail is not recieved, check RUT status manually in RMS'.format(id)
    send_mail(subject + '\n\n' + body)

def dev_mail(id, status, location):
    #message on change of device status
    subject = 'Subject: CREAMT_MONITOR_' + location
    if status:
        body = 'Scan Controller\nONLINE'.format(id)
    else:
        body = 'Scan Controller\nOFFLINE\n\nResetting: If an online e-mail is not recieved, check device status manually'
    send_mail(subject + '\n\n' + body)
