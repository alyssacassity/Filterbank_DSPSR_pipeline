#!/bin/bash
# run pam to scrunch in freq and time on all .ar files
pam -f 128 -T -p -d 0. -e ftp *.ar

# psredit DM back to real value
psredit -c dm=19.5 -e fix *.ftp

# smooth 
psrsmooth -W *.fix


