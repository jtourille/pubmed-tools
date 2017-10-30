# PubMed Tools

This repository regroups some tools for MEDLINE/PubMed data processing.

## Text extraction

To extract titles and abstracts from MEDLINE/PubMed citation records, first download the compressed files from 
the official MEDLINE/PubMed [website](https://www.nlm.nih.gov/databases/download/pubmed_medline.html).

Then, use this tool to extract titles and abstracts from the compressed files:

```bash
python main.py EXTRACT \
    --input_dir /path/to/downloaded/data \
    --output_dir /path/to/output/dir \
    -n <number-of-processes>
```