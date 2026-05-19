This is the output of %(anvi-compute-genome-similarity)s (which describes the level of similarity between all of the input genomes) or %(anvi-script-compute-ani-for-fasta)s (which describes the level of similarity between contigs in a fasta file).

{:.notice}
The output of %(anvi-compute-genome-similarity)s will only be in this structure if you did not input a %(pan-db)s. Otherwise, the data will be put directly into the additional data tables of the %(pan-db)s. The same is true of %(anvi-script-compute-ani-for-fasta)s.

This is a directory (named by the user) that contains both a %(dendrogram)s (NEWICK-tree) and a matrix of the similarity scores between each pair for a variety of metrics dependent on the program that you used to run %(anvi-compute-genome-similarity)s or %(anvi-script-compute-ani-for-fasta)s .

For example, if you used `fastANI` (the default ANI program), the output directory will contain matrices and, when clustering succeeds, Newick files for the following reports:

-`fastANI_ani.newick` and `fastANI_ani.txt`: contains the ANI values.

-`fastANI_alignment_fraction.newick` and `fastANI_alignment_fraction.txt`: contains the fraction of fragments that mapped.

-`fastANI_mapping_fragments.newick` and `fastANI_mapping_fragments.txt`: contains the number of mapped fragments.

-`fastANI_total_fragments.newick` and `fastANI_total_fragments.txt`: contains the total number of fragments considered.
