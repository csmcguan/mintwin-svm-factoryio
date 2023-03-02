#!/bin/bash

/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_attacker --type headless
/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_plc --type headless
/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_hmi --type headless
sh ./util/check-booted.sh factoryio_attacker factoryio_plc factoryio_hmi

/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_attacker take initialized --live
/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_plc take initialized --live
/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_hmi take initialized --live

sh ./util/stopvms.sh factoryio_attacker factoryio_plc factoryio_hmi
