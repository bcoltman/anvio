This program **provides information about each of the single-copy core genes in your %(contigs-db)s**.

Simply provide a %(contigs-db)s, and it will create a %(genes-stats)s file containing a variety of information about the single copy core genes in your database.

{:.notice}
This is kind of an old anvi'o script that we still keep around because history. But if you are here, you may also consider taking a look at the programs %(anvi-script-gen-hmm-hits-matrix-across-genomes)s and %(anvi-get-sequences-for-hmm-hits)s.

{{ codestart }}
anvi-script-gen_stats_for_single_copy_genes.py -c %(contigs-db)s
{{ codestop }}

The console output will tell you the total number of contigs, splits, and nucleotides in your %(contigs-db)s, while the text output will tell you the source, name, and e-value of each single-copy core gene.

You can get information from only single-copy core genes from a specific source. To see what sources are available in your %(contigs-db)s, run

{{ codestart }}
anvi-script-gen_stats_for_single_copy_genes.py -c %(contigs-db)s \
                                               --list-sources
{{ codestop }}
