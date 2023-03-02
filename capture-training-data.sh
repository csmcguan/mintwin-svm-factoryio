#!/bin/bash

# handle ctrl+c
close() 
{
  sh ./util/stopvms.sh factoryio_hmi factoryio_plc
  /mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
  exit 1
}

trap close INT

HMIUSR="hmi"
HMIPASS="password"

echo "[*] Capturing training data"
# start vms
sh ./util/startvms.sh factoryio_hmi factoryio_plc
sh ./util/check-booted.sh factoryio_hmi factoryio_plc

# start factoryio
/mnt/c/Program\ Files\ \(x86\)/Real\ Games/Factory\ IO/Factory\ IO.exe    \
"load:C:\Users\<user>\Documents\Factory IO\My Scenes\Production Line.factoryio" run &
sleep 400

# capture data
(/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
guestcontrol factoryio_hmi run			\
--username $HMIUSR				\
--password $HMIPASS				\
--wait-stdout					\
--wait-stderr					\
-- /usr/bin/timeout 400 /usr/bin/python3 	\
/home/hmi/data-capture/capture-from-plc.py training-data.csv) 2> /dev/null &

sleep 400
sh ./util/stopvms.sh factoryio_hmi factoryio_plc
/mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
