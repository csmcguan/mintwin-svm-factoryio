#!/bin/bash

for MACHINE in "$@"; do
  case $MACHINE in
    "factoryio_attacker")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe controlvm factoryio_attacker poweroff
      ;;
    "factoryio_plc")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe controlvm factoryio_plc poweroff
      ;;
    "factoryio_hmi")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe controlvm factoryio_hmi poweroff
      ;;
  esac
done
