#!/bin/bash
while :
do
	now=$(date +"%T")
	echo "Debut: $now"
	echo "START UPDATE POST"
	python updatePost.py
	wait
	echo "START UPDATE USER"
	python updateUser.py
	wait
	end=$(date +"%T")
	echo "END: $end"
done