# Drafted using ChatGPT

# Asks user to specify parent filepath and child filepath,
# Sets parent filepath to "read only"
# Creates a linked clone at the child filepath using the parent filepath as parent
# Then creates a new VM using the child filepath as storage, effectively creating a cloned VM

# Getting information from user
$ParentPath = Read-Host "Enter the full path to the parent .vhdx file"
$ChildPath = Read-Host "Enter the full path to the child .vhdx file"
$VMName = Read-Host "Enter the name for the cloned VM"

# Check if ParentPath exists
if (-Not (Test-Path -Path $ParentPath)) {
	Write-Error "Parent VHDX file not found at $ParentPath"
	exit
}

# Set parent disk to read-only if it isn't yet
try {
	$ParentFile = Get-Item -Path $ParentPath
	Set-ItemProperty -Path $ParentFile.FullName -Name IsReadOnly -Value $true
	Write-Host "Parent VHDX file has been set to read-only."
} catch {
	Write-Error: "Failed to set the parent VHDX file to read only: $_"
	exit
}

# create a differencing disk (linked clone)
try {
	New-VHD -Path $ChildPath -ParentPath $ParentPath -Differencing
	Write-Host "Linked clone created successfully at $ChildPath"
} catch {
	Write-Error "Failed to create linked clone: $_"
}

# create a new VM using new differencing disk
try {
	# 4GB RAM, 2VCPU, Gen 2, Secure Boot Off, Hyper-V WAN Network, linked clone as storage
	$VM = New-VM -Name $VMName -MemoryStartupBytes 4GB -Generation 2 
	Add-VMHardDiskDrive -VMName $VMName -Path $ChildPath
	Set-VMProcessor -VMName $VMName -Count 2
	Set-VMFirmware -VMName $VMName -EnableSecureBoot Off
	Add-VMNetworkAdapter -VMName $VMName -SwitchName "Hyper-V WAN"
	Write-Host "Virtual Machine '$VMName' created using '$ChildPath' as storage."
} catch {
	Write-Error "Failed to create or configure the VM: $_"
}
