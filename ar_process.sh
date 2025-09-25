#!/bin/bash
# run pam to scrunch in freq and time on all .ar files
pam -f 128 -T -p -d 0. -e ftp *.ar

# psredit DM back to real value
DM = 19.5
psredit -c dm=$DM -e fix *.ftp

# smooth profile
psrsmooth -W *.fix


