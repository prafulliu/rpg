#!/bin/bash

chmod +x stop.sh
./stop.sh

cd ../player/
chmod +x run.sh
./run.sh 
cd -

echo '**************************************'
echo "grep \"Traceback:\" ../log/*.log"
grep Traceback ../log/*.log
echo '**************************************'
echo "grep \"FATAL:\" ../log/*.log"
grep FATAL ../log/*.log
echo '**************************************'
echo "grep \"ERROR:\" ../log/*.log"
grep ERROR ../log/*.log
echo '**************************************'
echo "grep \"CRITICAL:\" ../log/*.log"
grep CRITICAL ../log/*.log
echo '**************************************'
