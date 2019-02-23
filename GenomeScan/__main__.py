__author__ = 'Jonathan Rubin'

import os
import sys
import argparse
import time
import subprocess

'''GenomeScan is a github repository that scans a genome fasta file for 
    motif hits using FIMO (part of MEME Suite)
'''


#GenomeScan source directory
srcdirectory = os.path.dirname(os.path.realpath(__file__))

#argparse to add arguments to this python package
parser = argparse.ArgumentParser(description=("GenomeScan uses FIMO (MEME Suite) to scan a genome for motif hits."),
                                usage=("GenomeScan -g /Full/Path/hg38.fa -m /Full/Path/HOCOMOCOv11.meme -e joru1876@colorado.edu -o /Full/Path/Output/"))

parser.add_argument('--genome','-g',default=False, metavar='',help=("REQUIRED. "
                        "A genome fasta file (.fa)"))

parser.add_argument('--motifs','-m',default=False,metavar='',help=("REQUIRED. "
                        "A meme formatted motif database file (.meme)"))

parser.add_argument('--email','-e',default=False,metavar='',help=("REQUIRED. "
                        "Email to send job information"))

parser.add_argument('--output','-o',default=False,metavar='',help=("REQUIRED. "
                        "Full path to output directory"))

parser.add_argument('--single','-s',default=False,metavar='',help=("OPTIONAL. "
                        "A motif within the motif database. Specify to run GenomeScan on a single motif."))

parser.add_argument('--thresh','-t', default='1e-6', metavar='', help=("OPTIONAL. "
                        "FIMO p-value cutoff [default: 1e-6]"))

parser.add_argument('--background','-bg', default='genome', metavar='', help=("OPTIONAL. "
                        "A markov background file (.txt). Set to False to use uniform background (not recommended) [default: genome]"))

parser.add_argument('--sleep', '-sl', default=100, metavar='', help=("OPTIONAL. "
                        "How long to sleep between checking status of jobs [defualt: 100]"))

parser.add_argument('--jobs', '-j', default=100, metavar='', help=("OPTIONAL. "
                        "How many jobs to submit at a time [defualt: 100]"))

parser.add_argument('--options', '-f', default='', metavar='', help=("OPTIONAL. "
                        "A string of options to provide FIMO [defualt: '-max-stored-scores 10000000 --text']"))

#Display help message when no args are passed.
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

#If user provided arguments, then parse them
genome = parser.parse_args().genome
motifs = parser.parse_args().motifs
email = parser.parse_args().email
output = parser.parse_args().output
single = parser.parse_args().single
thresh = parser.parse_args().thresh
background = parser.parse_args().background
sleep = int(parser.parse_args().sleep)
jobs = int(parser.parse_args().jobs)
options = parser.parse_args().options

#FUNCTIONS
#=============================================================================
def get_motifs(motifs=None, single_motif=False):
    if single_motif != False:
        return [single_motif]
    motiflist = []
    with open(motifs) as F:
        for line in F:
            motif = line.strip().split()[1]
            motiflist.append(motif)
    return motiflist

def check_jobs(running_jobs):
    status = [subprocess.check_output(["squeue", "-j", id]).decode('UTF-8').strip('\n').split()[-4] for id in running_jobs]
    updated_jobs = [running_jobs[i] for i in range(len(running_jobs)) if status[i]=='R']
    return updated_jobs
                
#Main Script
#=============================================================================
scriptdir = os.path.join(os.path.dirname(srcdirectory), 'scripts')
e_and_o = os.path.join(os.path.dirname(srcdirectory), 'e_and_o')

fimo_runner = os.path.join(scriptdir, 'fimo_run.sbatch')

if not os.path.isdir(output):
    os.makedirs(output)
motiflist = get_motifs(motifs=motifs, single_motif=single)

#Obtain markov background file
if background == 'genome':
    background = os.path.join(output, "markov_background.txt")
    markov_bg_command = "fasta-get-markov " + genome + " > " + background
    subprocess.check_output(markov_bg_command, shell=True)
elif not background:
    background = '--uniform--'

running_jobs = list()
for i, motif in enumerate(motiflist):
    fimo_command = ("fimo " + options 
                    + " --bgfile " + background
                    + " --thresh " + thresh 
                    + " -oc " + output 
                    + " --motif " + motif 
                    + " " + motifs
                    + " " + genome)
        
    sbatch_command = ["sbatch", 
                        "--job-name=fimo_" + motif,
                        "--mail-user=" + email, 
                        "--output=" + os.path.join(e_and_o,"%x.out"),
                        "--error=" + os.path.join(e_and_o,"%x.err"), 
                        "--export=fimo_command=" + fimo_command + ",output=" + os.path.join(output,motif),
                        fimo_runner]
    running_jobs.append(subprocess.check_output(sbatch_command).decode('UTF-8').strip('\n').split()[-1])
    while len(running_jobs) >= jobs:
        running_jobs = check_jobs(running_jobs)
        time.sleep(sleep)
        


