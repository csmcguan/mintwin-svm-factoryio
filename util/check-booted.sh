#!/bin/bash

ATKUSR="attacker"
HMIUSR="hmi"
PLCUSR="plc"
PASSWD="password"

for MACHINE in "$@"; do
  case $MACHINE in
    "factoryio_attacker")
      echo "Verifying that factoryio_attacker has booted..."
      while : ; do
        (/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe	\
        guestcontrol factoryio_attacker run	\
        --timeout 500		\
        --wait-stdout		\
        --wait-stderr		\
        --username $ATKUSR	\
        --password $PASSWD	\
        -- /bin/echo ) 2> /dev/null && echo "Done!" && break
        sleep 5
      done
      ;;
    "factoryio_hmi")
      echo "Verifying that factoryio_hmi has booted..."
      while : ; do
	(/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe	\
	guestcontrol factoryio_hmi run	\
        --timeout 500		\
        --wait-stdout		\
        --wait-stderr		\
	--username $HMIUSR	\
	--password $PASSWD	\
	-- /bin/echo ) 2> /dev/null && echo "Done!" && break
        sleep 5
      done
      ;;
    "factoryio_plc")
      echo "Verifying that factoryio_plc has booted..."
      while : ; do
	(/mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe	\
	guestcontrol factoryio_plc run	\
        --timeout 500		\
        --wait-stdout		\
        --wait-stderr		\
	--username $PLCUSR	\
	--password $PASSWD	\
	-- /bin/echo ) 2> /dev/null && echo "Done!" && break
        sleep 5
      done
      ;;
  esac
done
