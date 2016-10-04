#!/bin/bash

filename=${1%.*}
filename=$(echo $filename | cut -f2 -d "/")
segmentfilename=$filename".seg"
echo "Started Diarization...../"

java -Xmx2024m -jar lium_old/LIUM_SpkDiarization.jar --fInputMask=$1 --sOutputMask=diarization/$segmentfilename --doCEClustering --cMinimumOfCluster=1 $filename

#echo "Completed Diarization...../"


echo "Started Audio Segmentation...../"

./split_script.sh diarization/$segmentfilename $1

#echo "Completed Audio Segmentation...../"


echo "Started Audio Transcription...../"
python sentiment_analysis.py 

echo "Completed Audio Transcription...../"
