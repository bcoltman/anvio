# coding: utf-8
"""Interface for gene calling that uses `pyrodigal`."""

import multiprocessing.pool

import anvio
import anvio.fastalib as f
import anvio.utils as utils
import anvio.terminal as terminal
import anvio.constants as constants

from anvio.errors import ConfigError

try:
    import pyrodigal
except ImportError:
    raise ConfigError("Your anvi'o environment is missing the `pyrodigal` package. But it is easy to "
                      "solve. Please run `pip install pyrodigal` first.")

__author__ = "Developers of anvi'o (see AUTHORS.txt)"
__copyright__ = "Copyleft 2015-2024, the Meren Lab (http://merenlab.org/)"
__credits__ = []
__license__ = "GPL 3.0"
__version__ = anvio.__version__
__maintainer__ = "A. Murat Eren"
__email__ = "a.murat.eren@gmail.com"

run = terminal.Run()
progress = terminal.Progress()
pp = terminal.pretty_print


def predict(datum):
    contig_name, sequence, predictor = datum
    return (contig_name, predictor.find_genes(sequence))


class Pyrodigal:
    def __init__(self, args=None, progress=progress, run=run):
        self.progress = progress
        self.run = run
        self.args = args

        # user params
        A = lambda x: (args.__dict__[x] if x in args.__dict__ else None) if args else None
        self.prodigal_translation_table = A('prodigal_translation_table')
        self.prodigal_single_mode = A('prodigal_single_mode')
        self.num_threads = A('num_threads')

        self.gene_caller_name = 'pyrodigal'
        self.gene_caller_version = pyrodigal.__version__

    def process(self, fasta_file_path, output_dir):
        """Take the fasta file, run pyrodigal on it, and make sense of the output

        Returns a gene calls dict, and amino acid sequences dict.
        """

        if self.prodigal_translation_table:
            raise ConfigError("Unfortunately the `--prodigal-translation-table` parameter is not yet implemented :/ "
                              "This is mostly because anvi'o developers did not have enough expertise to test its use "
                              "and validity. If you are willing to help us implement this feature, please contact us "
                              "through Discord (it will be a simple change, but will require someone's supervision).")

        # preparations to set the predictor starting with a check of single vs meta mode
        if self.prodigal_single_mode:
            # if we are in 'single' mode, that means we will have to first explicitly train
            # the gene finder with one of the sequences in the FASTA file. assuming the user
            # knows what they're doing, all seqeunces in the input file will be coming from
            # the same organism. so, since we have to offer a single sequence, we are going
            # to select the longest sequence in the FASTA file
            longest_sequence = ''
            longest_sequence_length = 0
            fasta = f.SequenceSource(fasta_file_path)
            while next(fasta):
                if len(fasta.seq) > longest_sequence_length:
                    longest_sequence_length = len(fasta.seq)
                    longest_sequence = copy.deepcopy(fasta.seq)
            fasta.close()

            if len(longest_sequence) < 20000:
                raise ConfigError(f"We have a problem. You are calling prodigal with `--prodigal-single-mode` flag, most "
                                  f"likely becasue you are working with a single genome rather than a metagenome. Which "
                                  f"is great. But this mode requires a training step, which cannot be done with a sequence "
                                  f"that is shorter than at least 20,000 nucleotides long. However, the longest sequence in "
                                  f"your FASTA file is only {pp(longest_sequence_length)}. Which means, you will have to drop "
                                  f"the `--prodigal-single-mode` for this to work :/")

            self.predictor = pyrodigal.GeneFinder()
            self.predictor.train(longest_sequence)
        else:
            self.predictor = pyrodigal.GeneFinder(meta=True)

        # since the predictor is now set, next we will read all sequences into the memory :/
        data = []
        fasta = f.SequenceSource(fasta_file_path)
        while next(fasta):
            data.append((fasta.id, fasta.seq, self.predictor),)
        fasta.close()

        self.run.warning("Anvi'o will use 'pyrodigal' by Martin Larralde (doi:10.21105/joss.04296), which builds upon the "
                         "approach originally implemented by Hyatt et al (doi:10.1186/1471-2105-11-119), to identify open "
                         "reading frames in your data. If you publish your findings, please do not forget to properly credit "
                         "both work.", lc='green', header="CITATION")


        # let's learn the number of sequences we will work with early on and report
        num_sequences_in_fasta_file = len(data)

        # some nice logs.
        self.run.warning('', header=f'Finding ORFs using pyrodigal {pyrodigal.__version__}', lc='green')
        self.run.info('Number of sequences', pp(num_sequences_in_fasta_file))
        self.run.info('Procedure', 'Single Genome (with `--prodigal-single-mode`)' if self.prodigal_single_mode else 'Metagenome (without `--prodigal-single-mode`)')

        self.progress.new('Processing')
        self.progress.update(f"Identifying ORFs using {terminal.pluralize('thread', self.num_threads)}.")

        # key variables to fill in
        gene_calls_dict = {}
        amino_acid_sequences_dict = {}

        gene_callers_id = 0
        with multiprocessing.pool.Pool(self.num_threads) as pool:
            for contig_name, predicted_genes in pool.map(predict, data):
                for gene in predicted_genes:
                    gene_calls_dict[gene_callers_id] = {'contig': contig_name,
                                                        'start': gene.begin - 1,
                                                        'stop': gene.end,
                                                        'direction': 'f' if int(gene.strand) == 1 else 'r',
                                                        'partial': gene.partial_begin or gene.partial_end,
                                                        'call_type': constants.gene_call_types['CODING'],
                                                        'source': self.gene_caller_name,
                                                        'version': self.gene_caller_version}

                    amino_acid_sequences_dict[gene_callers_id] = gene.translate().replace('*', '')

                    gene_callers_id += 1

        self.progress.end()
        self.run.info('Result',
                      'Pyrodigal (%s) has identified %d genes.' % (pyrodigal.__version__,
                                                                  len(gene_calls_dict)),
                      nl_after=1)

        return gene_calls_dict, amino_acid_sequences_dict
