#!/bin/bash
# usage: bash ./batch_process.sh <filepath of output file> <number of images>


BATCH_SIZE=1200
COMMAND_OUTPUT="commands.txt"
MAX_PROCS=25
OUTPUT_FILENAME=$1
N=$2

if [ -e $COMMAND_OUTPUT ]
then
    rm $COMMAND_OUTPUT
fi

if [ -e $OUTPUT_FILENAME ]
then
    echo "$OUTPUT_FILENAME already exists. Abort in order not to overwrite it."
    exit 1
fi

for (( s=1; s<=$N; s=s+BATCH_SIZE ))
do
    e=$((s+BATCH_SIZE-1))
    e=$(($e > N ? N : $e))
    echo "$s - $e"
    echo "~/virtualenv-15.0.0/myVE/bin/python ./hog.py /home/xhan/train ~/kaggle/trainLabels.csv $s $e >> ${OUTPUT_FILENAME}_${s}" >> $COMMAND_OUTPUT
done

cat commands.txt | xargs -I CMD --max-procs=${MAX_PROCS} bash -c CMD
cat ${OUTPUT_FILENAME}_* > ${OUTPUT_FILENAME}
rm ${OUTPUT_FILENAME}_*
