#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10gb
#SBATCH --time=10:00:00
#SBATCH --output /scratch/Users/joru1876/e_and_o/%x.out
#SBATCH --error /scratch/Users/joru1876/e_and_o/%x.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=joru1876@colorado.edu


module load meme/4.12.0

### Run FIMO
$fimo_command > ${output}.txt

### Remove first column of fimo.txt output to convert to bed
cut -f 2- ${output}.txt > ${output}.bed

### Remove original fimo.txt output file
rm ${output}.txt


