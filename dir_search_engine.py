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


def get_answered_posting_list(query_term, inverted_index):
    filt_query_term = filter_string(query_term)

    if filt_query_term in inverted_index:
        ans_post_list = inverted_index[filt_query_term]
    else:
        ans_post_list = []

    return ans_post_list


def print_results(ans_post_list, document_list):
    print ("\n< Results >")
    if not ans_post_list:
        print ("No documents found!")
    else:
        for tup in ans_post_list:
            print (document_list[tup[0]])


def print_help(commands):
    padding = max( list(map(lambda x: len(x), commands.keys())) )
    print ("\n< Help >")
    # print ("For exit input: <;>.")
    # print ("Show the inverted index: <;index>")
    # print ("Show the document IDs: <;docid>")
    # print ("Help: <;help>")
    for k, v in commands.items():
        print (k + " " * (padding + 2 - len(k)) + "-", v)


commands = {
    "Exit": ";;",
    "Index": ";;index",
    "Docid": ";;docid",
    "Help": ";;help"
}


if __name__ == '__main__':
    # This is the directory in which we will make the search.
    if "-d" in sys.argv:
        collection_directory = sys.argv[sys.argv.index("-d") + 1]
    else:
        collection_directory = "."


    col_path = make_path_to_collection(collection_directory)

    doc_list = get_document_list(col_path)

    inv_index = build_inverted_index(col_path, doc_list)


    # print_inverted_index(inv_index)

    # print_docIds (doc_list)


    # Parse the query from user input.
    if "-q" in sys.argv:
        query = sys.argv[sys.argv.index("-q") + 1]
        print ("\nSearch: " + query)
        post_list = get_answered_posting_list(query, inv_index)
        print_results(post_list, doc_list)
        sys.exit(0)


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
            post_list = get_answered_posting_list(query, inv_index)
            print_results(post_list, doc_list)

        query = input("\nSearch: ")
