#!/bin/bash

INPUT="positive_bursts_1.csv"

# change source name as needed
while IFS= read -r line; do
    MJD=$(echo "$line" | grep -oP "J1541\+47_\K[0-9]+(?=_pow)")
    echo "$line" >> "${MJD}.csv"
done < "$INPUT"
