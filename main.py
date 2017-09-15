import argparse
import logging
import os
import sys

from pubmed.input import extract_text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Sub-commands", description="Valid sub-commands",
                                       help="Valid sub-commands", dest="subparser_name")

    # Extract titles and abstracts from PubMed files
    parser_extract = subparsers.add_parser('EXTRACT', help="Extract title and abstracts from PubMed XML files "
                                                           "(gz format)")
    parser_extract.add_argument("--input_dir", help="Input directory containing .gz files", dest="input_dir", type=str,
                                required=True)
    parser_extract.add_argument("--output_dir", help="Output directory where extracted text will be stored",
                                dest="output_dir", type=str, required=True)
    parser_extract.add_argument("-n", "--n_jobs", help="Number of processes", dest="n_jobs", type=int, default=1,
                                required=True)

    args = parser.parse_args()

    if args.subparser_name == "EXTRACT":

        # Checking if input path exists
        if not os.path.isdir(os.path.abspath(args.input_dir)):
            raise NotADirectoryError("The input path you specified does not exist")

        # Checking if output path exists
        if not os.path.isdir(os.path.abspath(args.output_dir)):
            raise NotADirectoryError("The output path you specified does not exist")

        # Logging to stdout
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s')

        # Launching main process
        extract_text(args.input_dir, args.output_dir, n_jobs=args.n_jobs)
