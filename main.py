import argparse
import logging
import os
import shutil
import sys
import time
from datetime import timedelta

from pubmed.input import extract_text
from pubmed.tools import ensure_dir

if __name__ == "__main__":

    start = time.time()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        title="Sub-commands",
        description="Valid sub-commands",
        help="Valid sub-commands",
        dest="subparser_name",
    )

    # Extract titles and abstracts from PubMed files
    parser_extract = subparsers.add_parser(
        "EXTRACT",
        help="Extract title and abstracts from PubMed XML files "
        "(gz format)",
    )
    parser_extract.add_argument(
        "--input-dir",
        help="Input directory containing .gz files",
        dest="input_dir",
        type=str,
        required=True,
    )
    parser_extract.add_argument(
        "--output-dir",
        help="Output directory where extracted text will be stored",
        dest="output_dir",
        type=str,
        required=True,
    )
    parser_extract.add_argument(
        "-n",
        "--n-jobs",
        help="Number of processes",
        dest="n_jobs",
        type=int,
        default=1,
        required=True,
    )
    parser_extract.add_argument(
        "--overwrite",
        help="Override output directory if it already exists",
        action="store_true",
        dest="overwrite",
    )

    args = parser.parse_args()

    if args.subparser_name == "EXTRACT":

        # Checking if input path exists
        if not os.path.isdir(os.path.abspath(args.input_dir)):
            raise NotADirectoryError("The input path does not exist")

        # Checking if output path exists
        if not args.overwrite:
            if os.path.isdir(os.path.abspath(args.output_dir)):
                raise IsADirectoryError(
                    "The output path already exists. Use the --overwrite flag to overwrite the "
                    "directory."
                )

        if os.path.isdir(os.path.abspath(args.output_dir)):
            shutil.rmtree(os.path.abspath(args.output_dir))

        ensure_dir(os.path.abspath(args.output_dir))

        # Logging to stdout
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format="%(asctime)s %(message)s",
        )

        # Launching main process
        extract_text(args.input_dir, args.output_dir, n_jobs=args.n_jobs)

    end = time.time()

    logging.info(
        "Done ! (Time elapsed: {})".format(
            timedelta(seconds=round(end - start))
        )
    )
