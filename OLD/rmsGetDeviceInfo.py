import rmsApiReq, requests, json


def device_request():
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI0ZTBkZWI0MzZiZmVmZjdmMjk5MTQ1MGYzY2Q2NTdlZTRhNGE0MmUzNWQ0YTZiNDhlY2M3YTRkNjQ5YTNlZTdmY2RiYmZjODMyMWNhMTcwNSIsImlzcyI6Imh0dHBzOlwvXC9ybXMudGVsdG9uaWthLW5ldHdvcmtzLmNvbVwvYWNjb3VudCIsImlhdCI6MTY1NzYzMDUzNywibmJmIjoxNjU3NjMwNTM3LCJzdWIiOiIxNzYzNiIsImNsaWVudF9pZCI6IjkxMjNlYTY2LTJmMWQtNDM5Yy1iMWMyLTMxMWFjMDEwYWFhZCIsImZpcnN0X3BhcnR5IjpmYWxzZX0.N5DKt6cBBgb7dqXA5vNv1oQ8e0QwoP_rshv5nN0a2f9nZtI6q0EsozL6aIdWHyEpvEuTM4Fyb6pR3AgMrbRQpRCc-VyDJyY4ynXrO1bqbTd0IWLLbDHMl5PnvNm0WPkuKJ8WUK_4TS1PFeI9p6BVNAqrR0NlCxRtzxWgG_IC1Fa5p3SiOXv5Dgqgyea5j03yEGHZFz_olzlNt4gwhEIW4Cif1uQ71zw5drv86NSazv9WwTJ6I1igDHD54VZcqEYhn9d4-ZqUjh9I8YV68vZWAkCvxuY9nYpJuKFlb8-du5PWe4JtlfQEN7uiCOOq0E5jof4PSM2KgGEmbzevHmGkiw'
    headers = {"accept":"application/json", "Authorization":"Bearer " + access_token}
    api_request_url = 'https://rms.teltonika-networks.com/api/devices/'
    try:
        r = requests.get(api_request_url, headers=headers)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as err:
        print ("Oops: Request Error",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)   

r = device_request()

data = json.loads(r.text)
for device in data['data']:
    print('-----------------------------------')
    print('Name: ', device['name'])
    print('id: ', device['id'])
    print('model: ', device['original_model'])
    print('sn: ', device['serial'])
    print('ip: ', device['wan_ip'])
print('-----------------------------------')


deviceID = 273746

print(rmsApiReq.get_mobile_ip(deviceID))

deviceID = 354389

print(rmsApiReq.get_mobile_ip(deviceID))

