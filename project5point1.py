## SYS-350-01 Fall 2024 at Champlain College
## Jacob Williams
## Project: Milestone 5- More Automation with PyVMomi
## 10/26/2024

## importing dependencies...
import getpass
import json
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from datetime import datetime

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
    si=SmartConnect(host=vcenterhost, user=vcenteradmin, pwd=passw, sslContext=s) # initiating connection to vCenter
    print(f"successful login to {vcenterhost} as {vcenteradmin}")
    aboutInfo=si.content.about
    print(aboutInfo) # prints VCenter instance information
    print(aboutInfo.fullName)

    ## This menu section is from Andy Dolinski - Making a menu in python on youtube
    def menu():
        print("[1] vCenter Info")
        print("[2] Session Details")
        print("[3] VM Details")
        print("[4] Power On a VM")
        print("[5] Power Off a VM")
        print("[6] Take a VM Snapshot")
        print("[7] Restore a VM to Latest Snapshot")
        print("[8] Clone a VM")
        print("[9] Delete a VM")
        print("[0] Exit the program.")

    menu()
    option = int(input("Enter your option..."))

    while option != 0:
        ## prints same instance info as startup
        if option == 1:
            print("vCenter info option selected...")
            print(aboutInfo)

        elif option == 2: ## session details
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

            ## Gets the hostname of the vCenter server and prints
            print(f"host = {si._stub.host}")

            print("---------------------------")

        elif option == 3:
            ## drafted by ChatGPT
            ## prints all VMs managed by Vcenter
            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            print("VM details selected...")
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")

            ## asks user to enter VM name
            search_query = input("Enter the name of your VM (leave empty if you want all printed)").strip() ## strip removes any accidental spaces
            print()

            ## drafted by ChatGPT
            if search_query == "": ##blank input
                print("blank input, listing all VMs")
                print()
                for vm in vms:
                    vm_found = True #enable flag to avoid error msg later
                    print(f"Name: {vm.name}") ##retrieves and prints vm name 
                    print(f"State: {vm.runtime.powerState}") ##retrieves and prints power state
                    print(f"Number of CPUS: {vm.config.hardware.numCPU}") ##retrieves and prints number of CPUs
                    print(f"Memory Total: {vm.config.hardware.memoryMB / 1024} GB") ## retrieves number of megabytes and divides by 1024 to get Gigs
                    ip = vm.guest.ipAddress if vm.guest.ipAddress else "unavailable" ## defines ip as vm IP address, or as unavailable if it is unavailable.
                    print(f"IP Address: {ip}") ## prints IP whether it be an address or unavailable
                    print()
            else:
                ## variable to track if a valid VM was entered
                vm_found = False #if this flag is false, an error is thrown later
                for vm in vms:
                    if search_query.lower() == vm.name.lower():  ## compares query to container (after sanitizing to lowercase)
                        vm_found = True #enable flag to avoid error msg later
                        print(f"Name: {vm.name}") ##retrieves and prints vm name 
                        print(f"State: {vm.runtime.powerState}") ##retrieves and prints power state
                        print(f"Number of CPUS: {vm.config.hardware.numCPU}") ##retrieves and prints number of CPUs
                        print(f"Memory Total: {vm.config.hardware.memoryMB / 1024} GB") ## retrieves number of megabytes and divides by 1024 to get Gigs
                        ip = vm.guest.ipAddress if vm.guest.ipAddress else "unavailable" ## defines ip as vm IP address, or as unavailable if it is unavailable.
                        print(f"IP Address: {ip}") ## prints IP whether it be an address or unavailable
                
            if not vm_found: ##vm_found = False, then error message. This can happen if user searches for a VM that doesn't exist.
                print(f"VM {search_query} not found!")

        elif option == 4: #powering on VMs, recycles content from previous option
            ## drafted by ChatGPT
            ## with elements from instructor example
            ## prints all VMs managed by Vcenter
            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            print("VM power-on selected...")
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")

            ## asks user to enter VM name
            search_query = input("Enter the name the VM  you want to power-on (leave empty if you want to power-on all)").strip() ## strip removes any accidental spaces
            print()

            ## drafted by ChatGPT
            if search_query == "": ##blank input, meaning they want all VMs powered on
                print("No input provided, powering on all VMs...")
                confirm = input("Are you sure about this? (Y/N:)") #Gets confirmation from user
                if confirm in ["Y",]: #If user confirms
                    print()
                    for vm in vms: ##for all VMs
                        vm_found = True #need this to prevent error later.
                        if vm.runtime.powerState == 'poweredOff': #checks VM powerstate
                            task = vm.PowerOn() #powers on VM
                            print(f"Powering on {vm.name}...") ##tells user
                        else: ## for machines already powered-on
                            print(f"{vm.name} is already on.")
                else:
                    print("Operation cancelled. No changes made") #If user enters N or anything other than Y
                    vm_found = True #need this 2 prevent error

            else:
                ## variable to track if a valid VM was entered
                vm_found = False #if this flag is false, an error is thrown later
                for vm in vms:
                    if search_query.lower() == vm.name.lower():  ## compares query to container (after sanitizing to lowercase)
                        vm_found = True #enable flag to avoid error msg later
                        if vm.runtime.powerState == 'poweredOff': #checks VM powerstate
                            task = vm.PowerOn() #powers on VM
                            print(f"Powering on {vm.name}...")
                        else:
                            print(f"{vm.name} is already on")
                
            if not vm_found: ##vm_found = False, then error message. This can happen if user searches for a VM that doesn't exist.
                print(f"VM {search_query} not found!")
            
        elif option == 5: # Powering off VM, copied mostly from previous option with inverted power options
            ## drafted by ChatGPT
            ## plus elements from instructor's example
            ## prints all VMs managed by Vcenter
            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            print("VM power-off selected...")
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")

            ## asks user to enter VM name
            search_query = input("Enter the name the VM  you want to power-off (leave empty if you want to power-off all)").strip() ## strip removes any accidental spaces
            print()

            ## drafted by ChatGPT
            if search_query == "": ##blank input
                print("No input provided, powering off all VMs...")
                confirm = input("Are you sure about this? (Y/N:)") #Gets confirmation from user
                if confirm in ["Y",]: #If user confirms
                    print()
                    for vm in vms:
                        vm_found = True #need this to prevent error later.
                        if vm.runtime.powerState == 'poweredOn': #checks VM powerstate
                            task = vm.PowerOff() #powers off VM
                            print(f"Powering off {vm.name}...")
                        else:
                            print(f"{vm.name} is already off.")
                else:
                    print("Operation cancelled. No changes made") #If user enters N or anything other than Y
                    vm_found = True #need this 2 prevent error

            else:
                ## variable to track if a valid VM was entered
                vm_found = False #if this flag is false, an error is thrown later
                for vm in vms:
                    if search_query.lower() == vm.name.lower():  ## compares query to container (after sanitizing to lowercase)
                        vm_found = True #enable flag to avoid error msg later
                        if vm.runtime.powerState == 'poweredOn': #checks VM powerstate
                            task = vm.PowerOff() #powers on VM
                            print(f"Powering off {vm.name}...")
                        else:
                            print(f"{vm.name} is already off")
                
            if not vm_found: ##vm_found = False, then error message. This can happen if user searches for a VM that doesn't exist.
                print(f"VM {search_query} not found!")

        elif option == 6: ## taking a snapshot.
            ## we take some elements from previous steps
            ## drafted by ChatGPT, plus some elements from Michael Rice's pyvmomi community sample: create_snapshot.py
            ## githhub.com/vmware/pyvmomi-community-samples/blob/master/samples/create_snapshot.py

            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            print("Take a snapshot selected...")
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")

            ## asks user to enter VM name
            search_query = input("Enter the name of the VM you want a new snapshot of:").strip() #to elminiate blank chars
            print()
            ## didn't implement the "do all" option on this feature because I have been having trouble with storage space limitation.

            ## drafted by ChatGPT
            vm_found = False # if this flag is false, and error is thrown later
            for vm in vms:
                if search_query.lower() == vm.name.lower(): ## compares query to container (after sanitizing to lowercase)
                    vm_found = True ## sets flag to avoid error later
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #creates a timestamp at current date and time in the form of YYYYMMDD_HHMMSS
                    ## create a snapshot which includes the vm's name and a timestamp in the title, and includes the VM's memory state, and no quiescing.
                    task = vm.CreateSnapshot_Task(name=f"py_Snapshot_{vm.name}_{timestamp}", description="Created using Pyvmomi", memory=True, quiesce=False)
                    print(f"Created snapshot for {vm.name}...") #message that snapshot was created.
                
            if not vm_found: #If a VM that doesn't exist is entered
                print(f"VM {search_query} not found!")

        elif option == 7: # restore the most recent snapshot of a VM
            ## drafted using combination of chatGPT
            ## and pyvmomi community sample: snapshot_operations.py by Abdul Anshad
            ##https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/snapshot_operations.py

            ## takes elements from previous steps
            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            print("Restore VM snapshot selected...")
            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")
            
            ## asks user to enter VM name
            search_query = input("Enter the name of the VM you want to restore the most recent snapshot of...")
            print()

            vm_found = False ##variable to track if a valid VM was entered
            for vm in vms:
                if search_query.lower() == vm.name.lower(): ## compares query to container (after sanitizing to lowercase)
                    vm_found = True ##must enable this to dodge error later
                    if vm.snapshot is None:
                        print(f"{vm.name} has no snapshots!")
                    else:
                        lastsnapshot = vm.snapshot.rootSnapshotList[-1] ##identifying most recent snapshot
                        print(f"Restoring snapshot {lastsnapshot.name} for VM {vm.name}...") ##tells user which snapshot is restoring for which machine
                        task = lastsnapshot.snapshot.RevertToSnapshot_Task() ##performs the action of reverting VM to last snapshot

                
            if not vm_found: #If a VM that doesn't exist is entered
                print(f"VM {search_query} not found!")

        elif option == 8: ## clone VM (creates full (not linked) clone of VM)
            ## takes elements from previous steps
            ## combination of ChatGPT
            ## and pyvmomi community sample: clone_vm.py by Dann Bohn

            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            print("Clone a VM selected...")
            ## drafted by ChatGPT
            ## prints the name of each VM in the container
            
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")
            
            ## asks user to enter VM name
            search_query = input("Enter the name of the VM you want to clone:") 
            vm_found = False ##variable to track if a valid VM was entered
            ## asks user for clone name
            clone_name = input("Enter the name for the new cloned VM:")
            print()

            for vm in vms:
                if search_query.lower() == vm.name.lower(): ## compares query to container (after sanitizing to lowercase)
                    vm_found = True ##must enable this to dodge error later
                    vm_folder = vm.parent ##finds directory of VM parent folder
                    vm_resource_pool = vm.resourcePool ## specifying resource pool (same as source ppol for now)

                    clone_spec = vim.vm.CloneSpec(
                        location=vim.vm.RelocateSpec(pool=vm_resource_pool), ##specifies destination of VM's files on datastore
                        powerOn=False, #do not immediately start VM up
                        template=False #we are not using any template
                    )

                    print(f"Cloning VM {vm.name} to create new VM {clone_name}") ##tells user it has initiated cloning process
                    print()

                    task = vm.CloneVM_Task( ##start up the clone
                        folder=vm_folder, ##defines clone destination as the same folder as parent
                        name=clone_name, ## names the new VM the clone_name input from earlier
                        spec=clone_spec) ##implements the specifications we defined in clone_spec
                    
                    print(f"VM clone task initiated!") #once task is started

            if not vm_found: #if user searches for nonexistent VM
                print(f"VM {search_query} not found!")

        elif option == 9: ## delete a VM
            ## takes elements from previous steps
            ## combination of ChatGPT
            ## and pyvmomi community sample: destroy_vm.py by Michael Rice
            ## https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/destroy_vm.py

            ## defines container as root folder for VMs
            container = si.content.rootFolder
            ## object type should be VMs
            view_type = [vim.VirtualMachine]
            ##container view for VMs (true means we cycle through the entire inventory)
            vm_view = si.content.viewManager.CreateContainerView(container, view_type, True)
            ## create list vm of all VMs in container
            vms = vm_view.view

            print("Delete VM selected...")
            
            ## prints list of VMs managed by Vcenter
            if vms:
                print("VMs managed by vcenter:")
                for vm in vms:
                    print(vm.name)
            else:
                ## or if none are in the container
                print("no VMs detected!")
            
            ## asks user to enter VM name
            search_query = input("Enter the name of the VM you want to delete:") 
            print()
            vm_found = False ##variable to track if a valid VM was entered

            for vm in vms:
                if search_query.lower() == vm.name.lower(): ##sanitizes input to lowercase
                    vm_found = True
                    ## gets Y/N confirmation from user
                    confirm = input(f"Are you sure you want to delete VM {vm.name}? This is irreversible, and the VM's storage will be irrecoverable. (Y/N):")
                    if confirm == 'Y':
                        print(f"Deleting VM {vm.name}...") ## tells user what it is doing
                        task = vm.Destroy_Task() ## tells Vcenter to delete VM
                        print(f"VM deletion initiated for {vm.name}...") ## tells user process has begun
                    else:
                        print("VM deletion has been cancelled.")

            if not vm_found: #if user searches for nonexistent VM
                print(f"VM {search_query} not found!")

        else:
            print("Invalid option!") ## if user picks a number with no assigned option.
        print()
        menu()
        option = int(input("Enter your option..."))

    print("thanks for using this program, goodbye!") ## if user picks 0 to exit

##if password is bad, throw error
except vim.fault.InvalidLogin as e:
    print("Error: Incorrect vCenter password!")

## if there is a different kind of error, throw a unexpected error
except Exception as e:
    print(f"unexpected error: {e}")

finally:
     # Disconnect if connected
    if 'si' in locals():
        Disconnect(si)