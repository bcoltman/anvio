This artifact represents **a JSON-formatted file derived from a %(reaction-network)s**.

The program, %(anvi-get-metabolic-model-file)s, produces this file from the %(reaction-network)s stored in a %(contigs-db)s or %(pan-db)s. The genes, reactions, and metabolites predicted to be involved in metabolism can be inspected in this file, which is formatted for compatability with software used for flux balance analysis, such as [COBRApy](https://opencobra.github.io/cobrapy/).

%(anvi-get-metabolic-model-file)s includes an "objective function" as the first entry of the "reactions" section of the file, a prerequisite for flux balance analysis. The objective function represents the biomass composition of metabolites in the ["core metabolism" of *E. coli*](http://bigg.ucsd.edu/models/e_coli_core).
