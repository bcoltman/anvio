
This program uses the user's similarity metric of choice to calculate the similarity between the input genomes.

The currently available programs for calculating similarity metrics include, chosen can be chosen with `--program`:
- [fastANI](https://github.com/ParBLiSS/FastANI) to calculate average nucleotide identity (ANI)
- [sourmash](https://sourmash.readthedocs.io/en/latest/) to calculate the mash distance between genomes.  Though we provide this option, we don't recommend using sourmash for genome comparisons--it excels at other tasks--yet it remains as a legacy option.

### Input/Output

The expected input is any combination of %(external-genomes)s, %(internal-genomes)s, and text files that contains paths to %(fasta)s files that describe each of your genomes. This is a tab-delimited file with two columns (`name` and `path` to the fasta files, each of which is assumed to be a single genome).


The program outputs a directory with %(genome-similarity)s data. The specific contents will depend on how similarity scores are computed (specified with `--program`), but generally contains tab-separated files of similarity scores between genomes and related metrics.


You also have the option to provide a %(pan-db)s, in which case the output data will additionally be stored in the database as %(misc-data-layers)s and %(misc-data-layer-orders)s data. This was done in the [pangenomic tutorial](http://merenlab.org/2016/11/08/pangenomics-v2/#computing-the-average-nucleotide-identity-for-genomes-and-other-genome-similarity-metrics-too).

Here is an example run with fastANI from an %(external-genomes)s without any parameter changes:

{{ codestart }}
anvi-compute-genome-similarity -e %(external-genomes)s \
                               -o path/for/%(genome-similarity)s \
                               --program fastANI
{{ codestop }}

### Genome similarity metrics: parameters

Parameters have been divided up based on which `--program` you use.

#### fastANI

You can change any of the following fastANI parameters:

* The kmer size. The default is 16.

* The fragment length. The default is 3000.

* The minimum alignment fraction for fastANI to report a result. The default is 0.25.

#### sourmash

You have the option to change the `kmer-size`. This value should depend on the relationship between your samples. The default is 31 ([as recommended by sourmash for genus-level distances](https://sourmash.readthedocs.io/en/latest/using-sourmash-a-guide.html), but we found that 13 most closely parallels the results from an ANI alignment.

You can also set the compression ratio for your fasta files. Decreasing this from the default (1000) will decrease sensitivity.

### Other Parameters

Once calculated, the similarity matrix is used to create dendrograms via hierarchical clustering, which are stored in the output directory (and in the %(pan-db)s, if provided). You can choose to change the distance metric or linkage algorithm used for this clustering.


If you're getting a lot of debug/output messages, you can turn them off with `--just-do-it` or helpfully store them into a file with `--log-file`.
