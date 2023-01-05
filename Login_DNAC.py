
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import prettyTables
from prettytable import PrettyTable
import os
import datetime

dnac_devices = PrettyTable(['device Type','Platform Id','Software Type','Software Version','serial No' ])
dnac_devices.padding_width = 1

dnac = {
    "host": "sandboxdnac.cisco.com",
    "port": 443,
    "username": "devnetuser",
    "password": "Cisco123!"
}
print("you are going to fetch details from DNAC with IP:",dnac["host"])

headers = {
              'content-type': "application/json",
              'x-auth-token': ""
          }

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dnac_login(host, username, password):
    url = "https://{}/api/system/v1/auth/token".format(host)
    print("login url",url)
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)
    print("token recoeved",response.text)
    return response.json()["Token"]


def network_device_list(dnac, token):
    url = "https://{}/api/v1/network-device".format(dnac['host'])
    headers["x-auth-token"] = token
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    print(data)
    for item in data['response']:
        dnac_devices.add_row(
            [item["type"], item["platformId"], item["softwareType"], item["softwareVersion"], item["serialNumber"]])


login = dnac_login(dnac["host"], dnac["username"], dnac["password"])
device_list = network_device_list(dnac, login)

print(dnac_devices)
path="/Users/vinsaini/Desktop/Git/"
file_name="/Users/vinsaini/Desktop/Git/DNAC_DATA.txt"
dir_list = os.listdir(path)
print("List of directories and files before creation:")
print(dir_list)
x = datetime.datetime.now()
file_data= "Last Execution Time for DNAC data is " + str(x) + "from "+ dnac["host"]
file=open(file_name,"w")
file.write(file_data)
file.close()