# Filterbank_DSPSR_pipeline
Scripts from Mehar to generate archive files with DSPSR and generate TOAs

1. Make a csv file for each MJD with positive_bursts_1.csv from CHIPSPIPE (I was too lazy to figure out how to get around this for now) with __split_csv.sh__

2. Make filterbank files around pulse using __Fitburst_fil_generator_decoupled.py__ . Need to change zoom window to be larger than the period. Run on the csvs with only real bursts (I made a copy of positive_burst_1.csv with RFI removed) - using __fil_gen_job.sh__

3. Run dspsr on the fils with __run_fil_dspsr.sh__ : `dspsr -k CHIME -nsub 1 -F 1 -E pulsar.par name.fil -O name` . pulsar.par is just the original par file. I think? it only works if it's renamed to pulsar.par

4. Run __ar_process.sh__ to scrunch, force it to have DM=0, and psredit back to DM value
-pam -f 128 -T -p -d 0. -e ftp *.ar
-psredit -c dm=$DM -e fix *.ftp

8. Optional (didn't work so well for me) smooth the profiles: psrsmooth -W *.fix

9. Extract TOAs with __run_pat.sh__  this uses the smoothed profile of one pulse as the template profile in pat. See below for making a combined profile.

10. Concatenate all the tim files for each into one `combined.tim` , with a grep to get rid of the FORMAT 1 lines.

Alternative to make a combined profile with all the pulses:
1. You might have to make all the single pulses have the same central frequency. Try #2 first and see if you have the error about the different central frequency before proceeding: psredit -c freq=601.757812 -m *.fix

2. Make a combined profile added.ftp (I didn't have that many pulses so I just did this in the command line, but you can use __make_template.batch__)
psradd -E pulsar.par -F *.fix -o added.ftp

3. Regenerate TOAs with this profile: __pat_command.batch__
