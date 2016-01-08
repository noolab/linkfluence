#!/bin/bash
while :
do
	python updatePost.py
	wait
	python updateUser.py
	wait
done