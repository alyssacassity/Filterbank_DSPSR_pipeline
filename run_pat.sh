#!/bin/bash

# loop
for file in *.ar; do
    # get base name from ar files
    NAME="${file%.ar}"
    
    echo "Processing $NAME..."
    
    # pat command to extract TOAs
    pat -A FDM \
        -e mcmc=0 \
        -C chan \
        -C subint \
        -C snr \
        -C wt \
        -f tempo2 IPTA \
        -X "-f CHIME -be CHIME -fe Rcvr_CHIME -pta NANOGrav" \
        "$NAME.fix" \
        -s "$NAME.fix.sm" \
        > "$NAME.tim"
done

