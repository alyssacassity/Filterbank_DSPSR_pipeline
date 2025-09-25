#!/bin/bash

pat -A FDM -e mcmc=0 -C chan -C subint -C snr -C wt -f tempo2 IPTA -X "-f CHIME -be CHIME -fe Rcvr_CHIME -pta NANOGrav" *.fix -s added.ftp > dspsr_added_profile_template.tim
