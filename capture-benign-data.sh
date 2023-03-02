#!/bin/bash

# handle ctrl+c
ctrlc() {
  sh ./util/stopvms.sh factoryio_hmi factoryio_plc
  /mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
  exit 1
}

trap ctrlc INT

HMIUSR="hmi"
HMIPASS="password"

# start vms
sh ./util/startvms.sh factoryio_hmi factoryio_plc
sh ./util/check-booted.sh factoryio_hmi factoryio_plc

# start factoryio
/mnt/c/Program\ Files\ \(x86\)/Real\ Games/Factory\ IO/Factory\ IO.exe    \
"load:C:\Users\hmcgu\Documents\Factory IO\My Scenes\Production Line.factoryio" run &
sleep 1m

for BENIGN in $(seq 0 49); do
  echo "[*] Capturing benign $BENIGN"

  # capture data
  (/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
    guestcontrol factoryio_hmi run		\
    --wait-stdout				\
    --wait-stderr				\
    --username $HMIUSR				\
    --password $HMIPASS				\
    -- /usr/bin/timeout 400 /usr/bin/python3	\
    /home/hmi/data-capture/capture-from-plc.py benign$BENIGN.csv) 2> /dev/null &
    
  sleep 415
done
sh ./util/stopvms.sh factoryio_hmi factoryio_plc
/mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
