#!/bin/sh
#SBATCH --job-name=GenomeScan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10gb
#SBATCH --time=24:00:00
#SBATCH --output /scratch/Users/joru1876/GenomeScan/e_and_o/%x.out
#SBATCH --error /scratch/Users/joru1876/GenomeScan/e_and_o/%x.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=joru1876@colorado.edu

module load python/3.6.3
module load meme/4.12.0

GenomeScan=/scratch/Users/joru1876/GenomeScan/GenomeScan
genome=/scratch/Shares/public/genomes/Mus_musculus/UCSC/mm10/Sequence/WholeGenomeFasta/genome.fa
motifs=/scratch/Users/joru1876/TFEA/motif_databases/HOCOMOCOv11_full_MOUSE_mono_meme_format.meme
email=joru1876@colorado.edu
output=/Users/joru1876/InterferonResponseJupyter/Steinparzer2018/Data

### Run for a single motif
single=STAT1_MOUSE.H11MO.1.A
python3 $GenomeScan -s $single -g $genome -m $motifs -e $email -o $output

### Run for all motifs
### python3 $GenomeScan -g $genome -m $motifs -e $email -o $output
