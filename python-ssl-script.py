import requests
import socket
import ssl
import datetime
import json
def ssl_check():
    l=['google.com','fb.com']
    for hostname in l:
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=hostname,)
        conn.settimeout(3.0)
        try:
            conn.connect((hostname, 443))
        except:
            print((hostname)+" Connection Failed")
            continue
        ssl_info = conn.getpeercert()
        Exp_ON=datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        Days_Remaining= Exp_ON - datetime.datetime.utcnow()
        response=str((hostname)+" Expires ON:- %s\nRemaining:- %s" %(Exp_ON,Days_Remaining))
        print(response)
        if Days_Remaining<datetime.timedelta(days=30):
          webhooks(response,1)

def domains():
    d = {'ashar.com':datetime.date(2024,5,1)}
    j=0
    for i in d:
        days_remaining=d[i]-datetime.date.today()
        if days_remaining<datetime.timedelta(days=30):
            response=str("Domain "+list(d)[j]+" Expires On %s\nRemaining:- %s" %(d[i],days_remaining))
            webhooks(response,2)
        j+=1

def webhooks(message,op):
    ssl="webhook_link_here"
    domain="https://webhook.site/ff2a4faa-e7a8-44c7-bb0d-d4ac199c3dda"
    data = {"msgtype": "text", "text": {"content": message}}
    if op==1:
        r = requests.post(ssl, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    else:
        r = requests.post(domain, data=json.dumps(data), headers={'Content-Type': 'application/json'})
