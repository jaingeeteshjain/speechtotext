#!/bin/bash
filename=${2%.*}
filename=$(echo $filename | cut -f2 -d "/")
echo $filename
cat $1 | cut -f 3,4,8 -d " " | \
       	while read LINE ; do \

		
		start=`echo $LINE | cut -f 1 -d " " | perl -npe '$_=$_/100.0'`; \
                len=`echo $LINE | cut -f 2 -d " " | perl -npe '$_=$_/100.0'`; \
                sp_id=`echo $LINE | cut -f 3 -d " "`; \
                #timeformatted=`echo "s$start $len" | perl -ne '@t=split(); $start=$t[0]; $len=$t[1]; $end=$start+$len; printf("%08.3f-%08.3f\n", $$start,$$end);'` ; \

		if [ ! "$len" = "0" ]
		then
		echo $sp_id $start $len
		sox $2 segmentedwavfiles/${filename}_${start}_${len}_${sp_id}.wav trim $start $len
		fi
             
		

                
        done
