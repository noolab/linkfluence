#!/bin/bash

python listenTwitter.py $1
wait
python listenInsta.py $1
wait 
python listenFB.py $1
wait
