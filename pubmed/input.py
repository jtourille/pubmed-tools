import gzip
import os
import re

from joblib import Parallel, delayed
from lxml import etree

from .tools import remove_abs, ensure_dir, get_other_extension


def extract_text(input_path: str = None,
                 output_path: str = None,
                 n_jobs: int = 1) -> None:
    """
    Extract titles and abstracts from PubMed documents
    :param input_path: path to the PubMed corpus
    :param output_path: path where extracted text will be stored
    :param n_jobs: number of processes to use
    :return: None
    """

    processing_list = list()

    for root, dirs, files in os.walk(os.path.abspath(input_path)):
        for filename in files:
            if re.match("^.*\.gz$", filename):

                # For each compressed file, computing its sub-directory
                subdir = remove_abs(re.sub(os.path.abspath(input_path), "", root))

                # Computing the target dir and creating it
                target_dir = os.path.join(os.path.abspath(output_path), subdir)
                ensure_dir(target_dir)

                # Computing source and target file paths
                source_file = os.path.join(root, filename)
                target_file = os.path.join(target_dir, get_other_extension(filename, "txt"))

                # Appending to processing list
                processing_list.append((source_file, target_file))

    # Starting text extraction
    Parallel(n_jobs=n_jobs)(delayed(_process_one_file)(source_file, target_file)
                            for source_file, target_file in processing_list)


def _process_one_file(source_file: str = None,
                      target_file: str = None) -> None:
    """
    Process one compressed PubMed file
    The function is largely inspired by the script developed by Sampo Pyysalo and available at
    https://github.com/spyysalo/pubmed
    :param source_file: source PubMed file
    :param target_file: target txt file
    :return: None
    """

    # Parsing the xml file
    tree = etree.parse(gzip.open(source_file, 'rb'))

    # Finding all MedlineCitation elements within the file
    citations = tree.findall(".//MedlineCitation")

    with open(target_file, "w", encoding="UTF-8") as output_file:
        # Looping over MedlineCitation
        for citation in citations:

            citation_text = list()
            citation_title = list()

            # Finding Article element
            article = citation.find("Article")

            # Finding ArticleTitle element
            article_title = article.find("ArticleTitle")

            # Sometimes, the title is empty
            if article_title.text is not None:
                citation_title.append(article_title.text)

            # Finding the Abstract element
            abstract = article.find("Abstract")

            # No abstract, looking for "OtherAbstract" elements
            if abstract is None:
                other_abstracts = citation.findall("OtherAbstract")

                # Found "OtherAbstract" elements, keeping only the first one
                if len(other_abstracts) >= 1:
                    abstract = other_abstracts[0]

            # If there is an abstract
            if abstract is not None:
                # Fetching "AbstractText" elements
                abstract_texts = abstract.findall("AbstractText")

                # Depending on the number of elements in the abstract
                if len(abstract_texts) == 1:
                    # Case where there is one monolithic abstract
                    citation_text.append(abstract_texts[0].text)
                else:
                    # Structured abstract case, fetching section titles and sections texts
                    for section in abstract_texts:
                        section_text = list()
                        if "Label" in section.attrib:
                            section_text.append("{}:".format(section.attrib["Label"]))
                        if section.text:
                            section_text.append(section.text)
                        citation_text.append(" ".join(section_text))

            # Writing title and abstracts to file
            for title in citation_title:
                # Removing [ and ] characters
                output_file.write("{}\n".format(
                    re.sub(r"[\]\[]", "", title)))

            for text in citation_text:
                output_file.write("{}\n".format(text))
