#!/bin/bash
while :
do
	now=$(date +"%T")
	echo "Debut: $now"
	echo "START LISTENNIG BENETTON"
	./listen.sh "benetton"
	wait
	echo "START LISTENNIG DIESEL"
	./listen.sh "diesel"
	wait
	echo "START LISTENNIG GOLRANG"
	./listen.sh "golrang"
	wait
	echo "START LISTENNIG NOOLAB"
	./listen.sh "noolab"
	wait
	echo "START LISTENNIG SPRINGFIELD"
	./listen.sh "springfield"
	wait
	echo "START LISTENNIG"
	./listen.sh "safir"
	wait
	echo "START LISTENNIG SAFIRPERFUMERY"
	./listen.sh "safirperfumery"
	wait
	echo "START LISTENNIG SEPHORA"
	./listen.sh "sephora"
	wait
	end=$(date +"%T")
	echo "END: $end"
	echo "ROUND FINISH"
done


