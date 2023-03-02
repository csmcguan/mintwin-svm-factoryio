#!/bin/bash

# handle ctrl+c
close() 
{
  sh ./util/stopvms.sh factoryio_hmi factoryio_attacker factoryio_plc
  /mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
  exit 1
}

trap close INT

ATKUSR="attacker"
ATKPASS="password"
HMIUSR="hmi"
HMIPASS="password"


for ATKNUM in $(seq 0 6); do
  echo "[*] Launching attack $ATKNUM"

  # start vms
  sh ./util/startvms.sh factoryio_attacker factoryio_plc factoryio_hmi
  sh ./util/check-booted.sh factoryio_attacker factoryio_plc factoryio_hmi

  # start factoryio
  /mnt/c/Program\ Files\ \(x86\)/Real\ Games/Factory\ IO/Factory\ IO.exe    \
  "load:C:\Users\<user>\Documents\Factory IO\My Scenes\Production Line.factoryio" run &
  sleep 1m

  # launch attack
  (/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
    guestcontrol factoryio_attacker run		\
    --username $ATKUSR				\
    --password $ATKPASS				\
    -- /usr/bin/sudo 				\
    /usr/bin/python3				\
    /home/attacker/modbus-attacks/mitm.py	\
    --timeout 410				\
    --target1 192.168.56.1			\
    --target2 192.168.56.2			\
    --attack attack$ATKNUM			\
    --forward					\
    --interface enp0s3) 2> /dev/null &
  sleep 10

  # capture data
  (/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
    guestcontrol factoryio_hmi run			\
    --wait-stdout				\
    --wait-stderr				\
    --username $HMIUSR				\
    --password $HMIPASS				\
    -- /usr/bin/python3 			\
    /home/hmi/data-capture/capture-from-plc.py attack$ATKNUM.csv) 2> /dev/null &
    
    sleep 415
    sh ./util/stopvms.sh factoryio_attacker factoryio_plc factoryio_hmi
    /mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
    sleep 2m
done
