## importing dependencies...
import getpass
import json
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

## pulling vcenterhost and vcenteradmin from  vcenter-conf.json
## ChatGPT drafted this section for me.
with open('vcenter-conf.json', 'r') as file:
    data = json.load(file)
vcenterhost = data['vcenter'][0]['vcenterhost']
vcenteradmin = data['vcenter'][0]['vcenteradmin']
print(f"logging into {vcenterhost} as {vcenteradmin}...")

## This section taking from instructor's starter file
## Gets password from user
passw = getpass.getpass()
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE

## This section is was drafted by ChatGPT combined with some stuff from instructor's starter file.
try:
    ## if successful login, pring aboutInfo
    si=SmartConnect(host=vcenterhost, user=vcenteradmin, pwd=passw, sslContext=s)
    print(f"successful login to {vcenterhost} as {vcenteradmin}")
    aboutInfo=si.content.about
    print(aboutInfo)
    print(aboutInfo.fullName)

    ## This menu section is from Andy Dolinski - Making a menu in python on youtube
    def menu():
        print("[1] vCenter Info")
        print("[2] Session Details")
        print("[3] VM Details")
        print("[0] Exit the program.")

    menu()
    option = int(input("Enter your option..."))

    while option != 0:
        if option == 1:
            print("vCenter info option selected...")
            print(aboutInfo)
            menu()
            option = int(input("Enter your option..."))


        elif option == 2:
            print("Option 2 has been called!")

        elif option == 3:
            print("Option 3")

        else:
            print("Invalid option!")


        print()
        menu()
        option = int(input("Enter your option..."))

    print("thanks for using this program, goodbye!")

##

except vim.fault.InvalidLogin as e:
    print("Error: Incorrect vCenter password!")
except Exception as e:
    print(f"unexpected error: {e}")
finally:
     # Disconnect if connected
    if 'si' in locals():
        Disconnect(si)