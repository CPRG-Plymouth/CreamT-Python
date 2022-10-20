import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText

#### CreamT Module ####
import rmsApiReq


########### Used to send emails to selected reciepients using gmail API as university blocks SMTP ########### 

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'bscan.system@gmail.com'


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

    # get the Gmail API service
service = gmail_authenticate()

########### Email addresses of recipients ###########
destination = 'mark.symons@plymouth.ac.uk, timothy.poate@plymouth.ac.uk'

##### Function for RUT Status Email  #######
def rut_mail(id, status, location, IP):
    #message on change of rut status
    subject = 'Subject: CREAMT_MONITOR_' + location
    if status:
        body = 'RUT Device: ID [{}], [{}] [{}] \nONLINE'.format(id,location,IP)

    else:
        body = 'RUT Device: ID [{}] \nOFFLINE\n\nResetting: If an online e-mail is not recieved, check RUT status manually in RMS'.format(id)
    
    message = MIMEText(body)
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = subject

    message =  {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    service.users().messages().send(userId="me",body=message).execute()
        

#### Function for Controller status ######
def dev_mail(id, status, location, IP):
    #message on change of device status
    subject = 'Subject: BSCAN_MONITOR_' + location
    if status:
        body = 'Scan Controller [{}]\nONLINE'.format(IP)
    else:
        body = 'Scan Controller [{}]\nOFFLINE\n\nResetting: If an online e-mail is not recieved, check device status manually'.format(IP)

    message = MIMEText(body)
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = subject

    message =  {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    service.users().messages().send(userId="me",body=message).execute()
        
        
#rut_mail(id,status,location)        