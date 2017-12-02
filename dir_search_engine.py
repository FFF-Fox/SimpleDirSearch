from os import walk
from collections import Counter
import string
import sys


def get_document_list(collection_path):
    D = [] # List containing the documents of the collection

    # Fill D with the filenames of the given collection_path
    for (dirpath, dirnames, filenames) in walk(collection_path):
        D.extend(filenames)
        break

    return D


def get_file_contents(filepath):
    # Read the file and return it's contents as a whole string
    with open(filepath, 'r') as myfile:
        data = myfile.read().replace('\n', ' ')

    return data


def filter_string(input_string):
    # Convert the data to lowercase
    input_string = input_string.lower()
    # Strip punctuation
    table = str.maketrans({key: None for key in string.punctuation})
    out_string = input_string.translate(table)

    return out_string


def make_terms_list(data):
    new_data = filter_string(data)
    # Split the data in a list of terms
    terms = new_data.split()

    return terms


def make_path_to_collection(collection_directory):
    if collection_directory[-1] != "/":
        path_to_collection = collection_directory + "/"
    else:
        path_to_collection = collection_directory

    return path_to_collection


def build_inverted_index(path_to_collection, document_list):
    # Build the inverted index
    inverted_index = {}
    for i, doc in enumerate(document_list):
        doc_contents = get_file_contents(path_to_collection + doc)

        terms = make_terms_list(doc_contents)

        # Enable for Debugging
        # print ("doc"+str(i)+":", doc, "- terms:", terms)

        for term in terms:
            if (term not in inverted_index):
                inverted_index[term] = [i]
            else:
                inverted_index[term].append(i)

    # Merge the appearences, create the posting list and sort
    # it based on docId
    for term in inverted_index:
        C = Counter(inverted_index[term])
        inverted_index[term] = [(i, C[i]) for i in C]
        inverted_index[term].sort()

    return inverted_index


def print_inverted_index(inverted_index):
    terms = inverted_index.keys()
    L = max( list(map(lambda x: len(x), terms)) )
    print ("\n< Inverted Index >")
    for term in sorted(terms):
        padding = " " * (L - len(term))
        print (term + padding, inverted_index[term])


def print_docIds(document_list):
    print ("\n< Document IDs >")
    # L = max( list(map(lambda x: len(x), document_list)) )
    l = len(str(len(document_list)))
    for i, doc in enumerate(document_list):
        # Lpadding = " " * (L - len(doc))
        lpadding = " " * (l - len(str(i)))
        print (str(i) + lpadding + " - " + doc)


def get_term_docids(query_term, inverted_index):
    # filt_query_term = filter_string(query_term)

    if query_term in inverted_index:
        results_docids = [ tup[0] for tup in inverted_index[query_term] ]
    else:
        results_docids = []

    return results_docids


def process_query(query, inverted_index):
    and_terms = query.split("^")
    filt_terms = [ filter_string(x).strip() for x in and_terms ]
    # Debugging
    # print (filt_terms)
    sets = [ set( get_term_docids(term, inverted_index) ) for term in filt_terms ]

    doc_intersec = sets[0]
    for S in sets:
        doc_intersec &= S
        # Debugging
        # print (doc_intersec)

    return list(doc_intersec)

def print_results(results_docids, document_list):
    print ("\n< Results >")
    if not results_docids:
        print ("No documents found!")
    else:
        for i in results_docids:
            print (document_list[i])


def print_help(commands):
    padding = max( list(map(lambda x: len(x), commands.keys())) )
    print ("\n< Help >")
    for k, v in commands.items():
        print (k + " " * (padding + 2 - len(k)) + "-", v)


def cli():
    commands = {
        "Exit": ";;",
        "Index": ";;index",
        "Docid": ";;docid",
        "Help": ";;help"
    }

    print_help(commands)

    query = input("\nSearch: ")
    while query != commands["Exit"]:
        if query in commands.values():
            if query == commands["Help"]:
                print_help(commands)
            elif query == commands["Index"]:
                print_inverted_index(inv_index)
            elif query == commands["Docid"]:
                print_docIds(doc_list)
        else:
            result = process_query(query, inv_index)
            print_results(result, doc_list)

        query = input("\nSearch: ")


if __name__ == '__main__':
    # This is the directory in which we will make the search.
    if "-d" in sys.argv:
        collection_directory = sys.argv[sys.argv.index("-d") + 1]
    else:
        collection_directory = "."

    # Build the inverted index and keep the doc_list for later use.
    col_path = make_path_to_collection(collection_directory)
    doc_list = get_document_list(col_path)
    inv_index = build_inverted_index(col_path, doc_list)

    # Parse the query from user input.
    if "-q" in sys.argv:
        query = sys.argv[sys.argv.index("-q") + 1]
        print ("\nSearch: " + query)
        result = process_query(query, inv_index)
        print_results(result, doc_list)
        sys.exit(0)
    else:
        cli()

        # Testing process_query()
        # query = "b ^ hard"
        # result = process_query(query, inv_index)
        # print_results(result, doc_list)
