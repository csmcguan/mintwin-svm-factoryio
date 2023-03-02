#!/bin/bash

close() 
{
  sh ./util/stopvms.sh factoryio_attacker factoryio_plc factoryio_hmi
  PROC=$(ps aux | grep live-monitor.sh | grep -v grep | awk '{ print $2 }')
  if [ ! -z $PROC ]; then 
    kill $PROC
  fi

  exit 1
}

trap close INT

# start with a fresh file
if [ -f time.csv ]; then
  rm time.csv
fi

touch time.csv

for ATKNUM in $(seq 0 7); do
  sh live-monitor.sh $ATKNUM 
  PROC=$(ps aux | grep live-monitor.sh | grep -v grep | awk '{ print $2 }')
  if [ ! -z $PROC ]; then
    kill $PROC
  fi
  sleep 30
done
