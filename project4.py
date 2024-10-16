## importing dependencies...
import getpass
import json
import ssl
from pyVim.connect import SmartConnect

## pulling vcenterhost and vcenteradmin from  vcenter-conf.json
## ChatGPT drafted this section for me.
with open('vcenter-conf.json', 'r') as file:
    data = json.load(file)
vcenterhost = data['vcenter'][0]['vcenterhost']
vcenteradmin = data['vcenter'][0]['vcenteradmin']


def menu():
    print("[1] Option 1")
    print("[2] Option 2")
    print("[3] Option 3")
    print("[0] Exit the program.")

def option3():
    print("Option 3 has been called using a function!")
    ## This section taking from instructor's starter file
    passw = getpass.getpass()
    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s.verify_mode=ssl.CERT_NONE
    si=SmartConnect(host=vcenterhost, user=vcenteradmin, pwd=passw, sslContext=s)
    aboutInfo=si.content.about
    print(aboutInfo)
    print(aboutInfo.fullName)
    

menu()
option = int(input("Enter your option..."))

while option != 0:
    if option == 1:
        print("Option 1 has been called! JSON STUFF!")
        with open('vcenter-conf.json', 'r') as file:
            data = json.load(file)
        vcenterhost = data['vcenter'][0]['vcenterhost']
        vcenteradmin = data['vcenter'][0]['vcenteradmin']
        print(f"vcenterhost: {vcenterhost}")
        print(f"vcenteradmin: {vcenteradmin}")


    elif option == 2:
        print("Option 2 has been called!")
    elif option == 3:
        option3()
    else:
        print("Invalid option!")

    print()
    menu()
    option = int(input("Enter your option..."))

print("thanks for using this program, goodbye!")