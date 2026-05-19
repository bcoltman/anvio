#!/usr/bin/env python
"""A script to export a FASTA files from sequence sources and compute genome similarity matrices."""

import sys
from anvio.argparse import ArgumentParser

import anvio
import anvio.terminal as terminal
import anvio.genomesimilarity as genomesimilarity

from anvio.errors import ConfigError, FilesNPathsError


__copyright__ = "Copyleft 2015-2024, The Anvi'o Project (http://anvio.org/)"
__credits__ = []
__license__ = "GPL 3.0"
__version__ = anvio.__version__
__authors__ = ['ekiefl']
__tags__ = ['ani', 'dereplication', 'redundancy']
__requires__ = ['external-genomes', 'internal-genomes', 'pan-db']
__provides__ = ['genome-similarity']
__description__ = ("Export sequences from sequence sources and compute a similarity metric (e.g. ANI). If a Pan Database "
                   "is given anvi'o will write computed output to misc data tables of Pan Database")
__resources__ = [("In action in the pangenomic workflow tutorial", "http://merenlab.org/2016/11/08/pangenomics-v2/#computing-the-average-nucleotide-identity-for-genomes-and-other-genome-similarity-metrics-too")]


@terminal.time_program
def main():
    args = get_args()
    run = terminal.Run()

    try:
        d = genomesimilarity.program_class_dictionary[args.program](args)
        d.process()

        if anvio.DEBUG:
            import json
            for report in d.results:
                run.warning(None, header=report)
                print(json.dumps(d.results[report], indent=2))

        d.cluster()
        d.report()
        d.add_to_pan_db()
    except ConfigError as e:
        print(e)
        sys.exit(-1)
    except FilesNPathsError as e:
        print(e)
        sys.exit(-1)


def get_args():
    parser = ArgumentParser(description=__description__)

    group_INPUT = parser.add_argument_group('INPUT OPTIONS', "Tell anvi'o what you want.")
    group_INPUT.add_argument(*anvio.A('internal-genomes'), **anvio.K('internal-genomes'))
    group_INPUT.add_argument(*anvio.A('external-genomes'), **anvio.K('external-genomes'))
    group_INPUT.add_argument(*anvio.A('fasta-text-file'), **anvio.K('fasta-text-file'))

    group_OUTPUT = parser.add_argument_group('OUTPUT OPTIONS', "Tell anvi'o where to store your results.")
    group_OUTPUT.add_argument(*anvio.A('output-dir'), **anvio.K('output-dir', {'required': True }))
    group_OUTPUT.add_argument(*anvio.A('pan-db'), **anvio.K('pan-db', {'required': False, 'help': "This is\
                        totally optional, but very useful when applicable. If you are running this for\
                        genomes for which you already have an anvi'o pangeome, then you can show where\
                        the pan database is and anvi'o would automatically add the results into the\
                        misc data tables of your pangenome. Those data can then be shown as heatmaps\
                        on the pan interactive interface through the 'layers' tab."}))

    group_PROGRAM = parser.add_argument_group('Program', "Tell anvi'o which similarity program to run.")
    group_PROGRAM.add_argument('--program', type=str, help="Tell anvi'o which program to run to process genome similarity.\
                        For ANI, anvi'o uses fastANI. If you for some reason want to use mash similarity, you can use sourmash,\
                        but its really not intended for genome comparisons.",
                        choices=['fastANI','sourmash'], default='fastANI')

    group_FASTANI = parser.add_argument_group('fastANI Settings', "Tell anvi'o to tell fastANI what settings to set.\
                                                                   Only if `--program` is set to `fastANI`")
    group_FASTANI.add_argument('--fastani-kmer-size', type=int, default=16, help="Choose a kmer. The default is %(default)s.")
    group_FASTANI.add_argument('--fragment-length', type=int, default=3000, help="Choose a fragment length. The default is %(default)s.")
    group_FASTANI.add_argument('--min-fraction', type=float, default=0.25, help="Minimum fraction of alignment to be shared between genome pairs \
                                                                                to calculate ANI. If reference and query genome size differ, \
                                                                                the smaller one among the two is considered. The default is %(default)s.")

    group_SOURMASH = parser.add_argument_group('Sourmash Settings', "Tell anvi'o to tell sourmash what settings to set.\
                                                Only if `--program` is set to `sourmash`")
    group_SOURMASH.add_argument('--kmer-size', type=int, default=None, metavar='INT', help="Set the k-mer size for mash\
                        similarity checks. We found 13 in almost all cases correlates best with alignment-based ANI.")
    group_SOURMASH.add_argument('--scale', type=int, default=1000, metavar='INT', help='Set the compression ratio for\
                        fasta signature file computations. The default is 1000. Smaller ratios decrease sensitivity,\
                        while larger ratios will lead to large fasta signatures.')


    group_CLUSTERING = parser.add_argument_group('HIERARCHICAL CLUSTERING', "anvi-compute-genome-similarity outputs similarity\
                                   matrix files, which can be clustered into nice looking dendrograms to display the\
                                   relationships between genomes nicely (in the anvi'o interface and elsewhere).\
                                   Here you can set the distance metric and the linkage algorithm for that.")
    group_CLUSTERING.add_argument(*anvio.A('distance'), **anvio.K('distance', {'help': 'The distance metric for the hierarchical \
                                   clustering. The default is "%(default)s".'}))
    group_CLUSTERING.add_argument(*anvio.A('linkage'), **anvio.K('linkage', {'help': 'The linkage method for the hierarchical \
                         clustering. The default is "%(default)s".'}))

    group_OTHER = parser.add_argument_group('OTHER IMPORTANT STUFF', "Yes. You're almost done.")
    group_OTHER.add_argument(*anvio.A('num-threads'), **anvio.K('num-threads'))
    group_OTHER.add_argument(*anvio.A('just-do-it'), **anvio.K('just-do-it'))
    group_OTHER.add_argument(*anvio.A('skip-checking-genome-hashes'), **anvio.K('skip-checking-genome-hashes'))
    group_OTHER.add_argument(*anvio.A('log-file'), **anvio.K('log-file'))

    return parser.get_args(parser)


if __name__ == '__main__':
    main()
