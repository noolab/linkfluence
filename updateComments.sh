#!/bin/bash
while :
do
	now=$(date +"%T")
	echo "Debut: $now"
	echo "START UPDATE POST"
	python updateComments.py
	wait
	end=$(date +"%T")
	echo "END: $end"
done