# PubMed Tools

This repository regroups some tools for PubMed corpus processing.

## Text extraction

To extract titles and abstracts from the files, first download the compressed files from 
the official MEDLINE/PubMed [website](https://www.nlm.nih.gov/databases/download/pubmed_medline.html).

Then, use this tool to extract the text from the compressed files:

```bash
python main.py --input_dir /path/to/downloaded/data \
    --output_dir /path/to/output/dir \
    -n <number-of-processes>
```