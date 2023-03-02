#!/bin/bash

for MACHINE in "$@"; do
  case $MACHINE in
    "factoryio_attacker")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_attacker restore initialized
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_attacker --type headless
      ;;
    "factoryio_plc")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_plc restore initialized
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_plc --type headless
      ;;
    "factoryio_hmi")
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe snapshot factoryio_hmi restore initialized
      /mnt/c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe startvm factoryio_hmi --type headless
      ;;
  esac
done
