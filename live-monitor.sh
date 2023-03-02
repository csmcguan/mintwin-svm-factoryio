#!/bin/bash

close() 
{
  PREDICT=$(ps aux | grep live-predict.py | grep -v grep | awk '{ print $2 }') 
  if [ ! -z $PREDICT ]; then
    kill $PREDICT
  fi
  /mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
  sh ./util/stopvms.sh factoryio_attacker factoryio_plc factoryio_hmi
  rm ./util/monitor-true.csv ./util/monitor-pred.csv ./data-capture/log/live.csv 2> /dev/null

  exit 1
}

trap close INT

HMIUSR="hmi"
ATKUSR="attacker"
PASSWD="password"

ATKNUM=$1

# start factoryio
/mnt/c/Program\ Files\ \(x86\)/Real\ Games/Factory\ IO/Factory\ IO.exe    \
"load:C:\Users\<user>\Documents\Factory IO\My Scenes\Production Line.factoryio" run &
sleep 30

# start vms
sh ./util/startvms.sh factoryio_attacker factoryio_hmi factoryio_plc
sh ./util/check-booted.sh factoryio_attacker factoryio_hmi factoryio_plc

# capture data
touch ./data-capture/log/live.csv 

(/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
  guestcontrol factoryio_hmi run	\
  --wait-stdout				\
  --wait-stderr				\
  --username $HMIUSR               	\
  --password $PASSWD                 	\
  -- /usr/bin/python3			\
  /home/hmi/data-capture/capture-from-plc.py live.csv) 2> /dev/null &

# predict
python3 ./util/live-predict.py ./data-capture/log/live.csv &

sleep 30

echo "Launching attack $ATKNUM"
# launch attack
(/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe    \
guestcontrol factoryio_attacker run         \
--wait-stdout					\
--wait-stderr					\
--username $ATKUSR                          \
--password $PASSWD                         \
-- /usr/bin/sudo                            \
/usr/bin/python3                            \
/home/attacker/modbus-attacks/mitm.py       \
--timeout 405                               \
--target1 192.168.56.1                      \
--target2 192.168.56.2                      \
--attack attack$ATKNUM                      \
--forward                                   \
--interface enp0s3) 2> /dev/null &

sleep 400


# not identified
if [ $(wc -l < time.csv) -lt $((ATKNUM+1)) ]; then
  echo "-1" >> time.csv
fi

/mnt/c/Windows/WinSxS/wow64_microsoft-windows-taskkill_31bf3856ad364e35_10.0.19041.1_none_e5c3b6db2fced475/taskkill.exe /im Factory\ IO.exe /t /f
sh ./util/stopvms.sh factoryio_attacker factoryio_plc factoryio_hmi
PREDICT=$(ps aux | grep live-predict.py | grep -v grep | awk '{ print $2 }') 
if [ ! -z $PREDICT ]; then
  kill $PREDICT
fi
rm ./util/monitor-true.csv ./util/monitor-pred.csv ./data-capture/log/live.csv 2> /dev/null
