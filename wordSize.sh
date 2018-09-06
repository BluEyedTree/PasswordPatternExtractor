#!/bin/bash
# Basic while loop
counter=1
while [ $counter -le 20 ]
	do
	echo $counter
	echo $counter
	((counter++))
	count=`awk -v n=$counter '{for (i=1; i<=NF; i++) if (length($i) == n) print $i}' totalList.txt | wc -l`
	echo $count
	python -c "print (float($count)/24344391)*100"
	done
	echo All done

