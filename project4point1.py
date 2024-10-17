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
vcenterhost = data['vcenter'][0]['vcenterhost'] ## [0] for first element in vcenterhost
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

        elif option == 2:
            ## drafted by ChatGPT

            ## Using session manager to retrieve session details
            session_manager = si.content.sessionManager
            current_session = session_manager.currentSession

            print("Session Details selected...")
            print("---------------------------")

            ## Gets username from current session and prints
            print(f"username = {current_session.userName}")

            ## Gets IP from current session and prints
            print(f"ip = {current_session.ipAddress}")

            ## Gets the hostname of the vCenter server
            print(f"host = {si._stub.host}")

            print("---------------------------")

        elif option == 3:
            ## prints all VMs managed by Vcenter
            ## drafted by ChatGPT
            ## root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            ## prints the name of each VM in the container
            print("VM details selected...")
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")

            ## asks use to enter VM name
            search_query = input("Enter the name of your VM (leave empty if you want all printed)").strip()
            print()

            if search_query == "": ##blank input
                print("blank input, listing all VMs")
                print()
                for vm in vms:
                    vm_found = True #simply enabling this flag so it doesn't trigger something later.
                    print(f"Name: {vm.name}") ##retrieves and prints vm name 
                    print(f"State: {vm.runtime.powerState}") ##retrieves and prints power state
                    print(f"Number of CPUS: {vm.config.hardware.numCPU}") ##retrieves and prints number of CPUs
                    print(f"Memory Total: {vm.config.hardware.memoryMB / 1024} GB") ## retrieves number of megabytes and divides by 1024 to get Gigs
                    ip = vm.guest.ipAddress if vm.guest.ipAddress else "unavailable" ## defines ip as vm IP address, or as unavailable if it is unavailable.
                    print(f"IP Address: {ip}")
                    print()
            else:
                ## variable to track if a valid VM was entered
                vm_found = False
                for vm in vms:
                    if search_query.lower() == vm.name.lower():  ## compares query to container (after sanitizing to lowercase)
                        vm_found = True
                        print(f"Name: {vm.name}") ##retrieves and prints vm name 
                        print(f"State: {vm.runtime.powerState}") ##retrieves and prints power state
                        print(f"Number of CPUS: {vm.config.hardware.numCPU}") ##retrieves and prints number of CPUs
                        print(f"Memory Total: {vm.config.hardware.memoryMB / 1024} GB") ## retrieves number of megabytes and divides by 1024 to get Gigs
                        ip = vm.guest.ipAddress if vm.guest.ipAddress else "unavailable" ## defines ip as vm IP address, or as unavailable if it is unavailable.
                        print(f"IP Address: {ip}")
                
            if not vm_found:
                print(f"VM {search_query} not found!")




        else:
            print("Invalid option!")
        print()
        menu()
        option = int(input("Enter your option..."))

    print("thanks for using this program, goodbye!")

##if password is bad, throw error
except vim.fault.InvalidLogin as e:
    print("Error: Incorrect vCenter password!")

## if there is a different kind of error, throw a different error
except Exception as e:
    print(f"unexpected error: {e}")

finally:
     # Disconnect if connected
    if 'si' in locals():
        Disconnect(si)