# Spoofing Detection on Factory I/O
Modbus packet spoofing using unsupervised machine learning on Factory I/O

## Setup
Instructionas assume a Windows 10 setup. Factory I/O only runs on Windows

### 1. Install VirtualBox
Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) for Windows

### 2. Install Factory I/O
Install [Factory I/O](https://factoryio.com/). This will require a valid license.

### 3. Host Only Network
Create the following host only network
```192.168.56.0/24```

### 4. Virtual Machines
We use three virtual machines as part of the VM topology. All of them run [Debian GNU/Linux](https://www.debian.org/download). Name all VMs as they are listed here.

**factoryio_plc.** 
* Install Debian on the plc VM with the following login:
```username: plc
password: password```
* Install [OpenPLC Runtime](https://openplcproject.com/)
* Download the [control logic](https://openplc.discussion.community/post/production-line-scene-from-factory-io-fbd-11657885) and follow the instructions to upload it to OpenPLC.
* Put the plc VM on the host only network with a static IP 192.168.56.2

**factoryio_hmi**
* Install Debian on the hmi VM with the following login:
```username: hmi
password: password```
* Install the following dependencies
```sudo apt install -y make gcc linux-headers-$(uname -r) python3 python3-pip```
* Install PyModbus
```pip3 install -y pymodbus```
* Install VBox Guest Additions
  * Mount /dev/cdrom
```sudo mkdir /mnt/cdrom && sudo mount /dev/cdrom /mnt/cdrom```
  * Insert the Guest Additions CD under devices in the menu bar
  * Install the Guest Additions
```sudo /mnt/cdrom/VBoxLinuxAdditions.run```
* Create a shared folder
  * Add user to vboxsf group
```sudo usermod -aG vboxsf hmi```
  * Create the following directory
```sudo mkdir /home/hmi/data-capture/```
  * Create a shared folder between the folder you just created and the one with the same name from this repository
* Add the following line to /etc/sudoers to use sudo without a password
```hmi ALL=(ALL) NOPASSWD:ALL```
* Put the hmi VM on the host only network

**factoryio_attacker**
* Install Debian on the hmi VM with the following login:
```username: attacker
password: password```
* Install the following dependencies
```sudo apt install -y make gcc linux-headers-$(uname -r) python3 python3-pip```
* Install scapy
```pip3 install -y scapy```
* Install [NetfilterQueue](pip install NetfilterQueue)
* Install VBox Guest Additions
  * Mount /dev/cdrom
```sudo mkdir /mnt/cdrom && sudo mount /dev/cdrom /mnt/cdrom```
  * Insert the Guest Additions CD under devices in the menu bar
  * Install the Guest Additions
```sudo /mnt/cdrom/VBoxLinuxAdditions.run```
* Create a shared folder
  * Add user to vboxsf group
```sudo usermod -aG vboxsf attacker```
  * Create the following directory
```sudo mkdir /home/hmi/modbus-attacks/```
  * Create a shared folder between the folder you just created and the one with the same name from this repository
* Add the following line to /etc/sudoers to use sudo without a password
```attacker ALL=(ALL) NOPASSWD:ALL```
* Put the attacker VM on the host only network
