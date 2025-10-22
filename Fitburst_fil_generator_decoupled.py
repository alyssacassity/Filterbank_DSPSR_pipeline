# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:34:19 2024
Last update on Tue Oct 21 2025
Final version before removing debug test statements
@author: ktsan, msahota, acassity
"""
import glob
import argparse
import numpy as np
from sigpyproc.readers import FilReader
import matplotlib.pyplot as plt
from iqrm  import iqrm_mask

ignored_chans = ([0] + list(range(34,48)) + list(range(113,179)) +
                 list(range(185,211)) + list(range(218,255)) + list(range(554,569)) + list(range(584,597)) +
                 list(range(631,645)) + list(range(677,694)) + list(range(754,763))+list(range(788,792))+list(range(854,861))+list(range(873,876))+[887])

# Cuts a chunk of the .fil file for analysis
def singlecut(fil_name, t_start, disp_measure, fil_time, t_origin, isddp=False):
    fbfile = FilReader(fil_name)
    sub = '.fil'
    # Remove suffix from filename for naming .npz file later
    fil_short_name = [i for i in fil_name.split("/") if sub in i][0].removesuffix(sub)
    fbh = fbfile.header
    downsamp = 8
    dsampfreq = 8
    # Define variables
    t_block = 10
    nsamps = int(t_block/fbh.tsamp)
    nsamps = nsamps-nsamps%downsamp
    #t_start = 396.3
    start_samp = round(t_start/fbh.tsamp) # starting sample block
    fblock = fbfile.read_block(start_samp, nsamps)

    # Remove channels depending on MJD of file
    if (int(filmjd[ind])>=59091 and int(filmjd[ind])<59093):
        ignored_chans.extend(list(range(444,470)))
    elif int(filmjd[ind])>=59093:
        ignored_chans.extend(list(range(405,470)))
    elif int(filmjd[ind])>=59523:
        ignored_chans.extend(list(range(83,108)))
    ignored_chans.extend(list(range(380,520)))
    # Mask above channels
    # Mask all known RFI channels
    import copy
    fbt = copy.deepcopy(fblock)
    mn = np.mean(fbt, axis = 1)
    mask = (mn == 0)
    fbt[mask,:] = np.median(fbt[~mask,:])
    std_on = np.std(fbt, axis=1)
    iqrmmask,votes = iqrm_mask(std_on, threshold=1, ignorechans=ignored_chans)
    mask[iqrmmask] = True
    mask[ignored_chans] = True
    fbt[mask,:] = np.median(fbt[~mask,:])
    # Identify bad channels for masking and dedisperse data if needed
    if not isddp:
        fbt = fbt.dedisperse(dm=19.5)
        disp_measure = 0
    else:
        fbt = fbt
        disp_measure = 0
    # Downsample data by ratio downsamp and downsample frequency data by ratio downfreq
    fbt = fbt.downsample(downsamp,dsampfreq)
    fbt = fbt.normalise()
    # Further cut data down to 1 second block
    zoom_mid_sample = int(t_block/2/fbh.tsamp/downsamp)
    zoom_window = 0.3 #second
    zoom_window_samples = int(zoom_window/fbh.tsamp/downsamp)
    zoom_start_samp = int(zoom_mid_sample - zoom_window_samples/2)
    zoom_end_samp = int(zoom_mid_sample + zoom_window_samples/2)
    fbt_zoom = fbt[:, zoom_start_samp:zoom_end_samp]
    fbt = fbt_zoom
    time_bin0 = fbh.tstart + start_samp*fbh.tsamp/86400 + zoom_start_samp*fbh.tsamp*downsamp/86400
    #Populate metadata and burst_parameters dictionaries for generating .npz file
    metadata = dict(bad_chans = 0, freqs_bin0 = fbh.fch1, is_dedispersed = isddp,
                    num_time = zoom_window_samples, num_freq = fbh.nchans/dsampfreq,
                    times_bin0 = time_bin0,  res_time = fbh.tsamp*downsamp, res_freq = fbh.foff*dsampfreq)
    burst_parameters = dict(ref_freq = [600.2], amplitude = [np.log10(np.max(fbt))], arrival_time = [0.5],
                            burst_width = [0.02], dm = [disp_measure], dm_index = [-2],
                            scattering_index = [-4], scattering_timescale = [0.01], spectral_index = [0],
                            spectral_running = [0])


    # Plot data and save
    #Saves figure to .png image
    plt.figure()
    plt.imshow(fbt, aspect='auto',cmap="YlGnBu")
    plt.savefig(fil_short_name + '_' + str(fil_time) + '_' + str(t_origin) + '_test.png')
    plt.close()
    outfile = fil_short_name + '_' + str(fil_time) + '_' + str(t_origin) + ".fil"
    update_header = fbh.new_header({"filename": outfile,
                                    "tstart": time_bin0, 
                                    "tsamp": fbh.tsamp*downsamp,
                                    "nsamples": zoom_window_samples,
                                    "filenames": [outfile],
                                    "nsamples_files": [zoom_window_samples],
                                    "tstart_files": [time_bin0],
                                    "foff": fbh.foff*dsampfreq})    
    fbt.header = update_header
    fbt.to_file(filename=outfile)
    return fbh.tstart


# Load files for analysis (Read in names of candidates)
"""Use Argparse to enable command line inputs"""
parser = argparse.ArgumentParser()
parser.add_argument(
    'index', 
    action='store', 
    type=int,
    help='Index')
parser.add_argument(
    "pulse_path", 
    action="store", 
    type=str,
    help="Path to .csv file containing all the candidate pulses to be analyzed")
#
parser.add_argument(
    'fils_path', 
    action='store', 
    type=str,
    help='Path to all .fil files to be analyzed')

args = parser.parse_args()
ind = args.index
pulse_path = args.pulse_path
fils_path = args.fils_path
datafile = pulse_path
data = np.genfromtxt(datafile, delimiter=",", dtype=str)
files = data[:,0]
tstart_list = []
filtime = []
fildm = []
filmjd = []

# Find and analyze candidate files for pulsar, appends found .fil files to list of files to run by singlecut function
for file in files:
    file = file[file.find('cand'):]
    filparts = file.split('_')
    filtime.append(filparts[4])
    fildm.append(filparts[6])
    tstart_list.append(filparts[2])
    filmjd.append(str(int(float(filparts[2]))))
filfiles = glob.glob(fils_path + r'/J1541+47_*_pow.fil')
fils_to_run = []
for i in range(len(files)):
   for file in filfiles:
       if filmjd[i] in file:
            fils_to_run.append(file)
toa_list = []
singlecut(fils_to_run[ind], float(filtime[ind])-5, float(fildm[ind]), float(filtime[ind]), float(tstart_list[ind]))
