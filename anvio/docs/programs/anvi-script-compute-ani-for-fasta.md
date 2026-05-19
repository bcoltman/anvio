This program computes the average nucleotide identity between reads in a single fasta file using fastANI.

To compute the ANI (or other genome distance metrics) between two genomes in different fasta files, use %(anvi-compute-genome-similarity)s.

A default run of this program looks like this:

{{ codestart }}
anvi-script-compute-ani-for-fasta -f %(fasta)s \
                                  -o path/to/output
{{ codestop }}

You can change the fastANI kmer size, fragment length, and minimum alignment fraction if the defaults are not appropriate for your sequences.

You also have the option to change the distance metric (from the default "euclidean") or the linkage method (from the default "ward") or provide a path to a log file for debug messages.
