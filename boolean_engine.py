from os import walk, sep
import string


class BooleanEngine:
    def __init__(self, collection_path='.', excluded=[], rf=True):
        self.inverted_index = {}
        self.documents = []

        self.build_index_from(collection_path, excluded, rf)


    def make_doclist_from(self, collection_path, excluded=[], rf=True):
        """ Creates the list containing the paths for the documents in the collection.
            Inputs:
                collection_path: The path of the collection, from which the
                    inverted idex will be built.
                rf: Whether to check the current directory and all subsequent
                subdirectories, or just the current one.
                excluded: List of excluded files or paths.
        """
        self.documents = []

        # Fill self.documents with the paths of the files in the given
        # collection_path and it's subdirectories
        for (dirpath, dirnames, filenames) in walk(collection_path):
            self.documents.extend([ dirpath + sep + filename
                                    for filename in filenames
                                    if not any( ex in dirpath.split(sep)
                                                or ex == filename
                                                or ex == dirpath
                                                or ex == dirpath + sep + filename
                                                for ex in excluded )
                                    ])
            if not rf:
                break


    def file_contents_of(self, document):
        """ Read the file and return it's contents as a whole string, removing
            newline characters.
        """
        with open(document, 'r') as doc:
            contents = doc.read().replace('\n', ' ')

        return contents


    def filter_string(self, in_string):
        """ Convert the data to lowercase and remove punctuation.
            Input:
                in_string: A string.
            Output:
                out_string: The in_string converted to lowercase and stripped
                    of punctuation.
        """
        in_string = in_string .lower()

        table = str.maketrans({key: None for key in string.punctuation})
        out_string = in_string.translate(table)

        return out_string


    def terms_of(self, in_string):
        """ Get a list containing the individual words of the input string.
            Input:
                in_string: A string.
            Output:
                out_string: A list of strings, containing the individual
                terms of in_string.
        """
        filt_string = self.filter_string(in_string)

        terms = filt_string.split()

        return terms


    def add_to_index(self, document, doc_id=None):
        """ Index the document. If it's not in the collection, add it.
            Inputs:
                document: Path to the document
                doc_id: (Optional) The docId of the document. If ommitted,
                    the docid is inferred.
        """
        if doc_id is None:
            try:
                doc_id = self.documents.index(document)
            except ValueError:
                # If the document is not in the collection
                self.documents.append(document)
                doc_id = len(self.documents) - 1

        doc_contents = self.file_contents_of(document)

        terms = self.terms_of(doc_contents)

        for term in terms:
            if (term not in self.inverted_index):
                self.inverted_index[term] = [doc_id]
            else:
                if doc_id not in self.inverted_index[term]:
                    self.inverted_index[term].append(doc_id)


    def build_inverted_index(self):
        """ Build the inverted index from the documents in the collection. """
        # Fill the index with all the appearences of each term in every
        # document.
        for doc in self.documents:
            self.add_to_index(doc)


    def build_index_from(self, collection_path, excluded=[], rf=True):
        """ Build the inverted index from the given collection path. """
        self.make_doclist_from(collection_path, excluded, rf)
        self.build_inverted_index()


    def print_inverted_index(self):
        """ Prints the inverted index in an easy for the eye form. """
        terms = self.inverted_index.keys()
        try:
            L = max( list(map(lambda x: len(x), terms)) )
        except ValueError:
            L = 0

        print ("\n< Inverted Index >")
        for term in sorted(terms):
            padding = " " * (L - len(term))
            print (term + padding, self.inverted_index[term])


    def print_docIds(self):
        """ Prints the documents with their docIds in an easy for the eye form.
        """
        print ("\n< Document IDs >")
        l = len(str(len(self.documents)))
        for i, doc in enumerate(self.documents):
            lpadding = " " * (l - len(str(i)))
            print (str(i) + lpadding + " - " + doc)


    def answer(self, query):
        """ Answer a single term query of the user.
            Input:
                query: String containing the query term of the user.
            Output:
                doc_ids: A list containing the docIds of the resulting documents.
        """
        query = query.strip()

        neg = False
        try:
            if query[0] == '!':
                neg = True
        except IndexError:
            pass

        filt_query = self.filter_string(query)

        if filt_query in self.inverted_index:
            doc_ids = self.inverted_index[filt_query]
        else:
            doc_ids = []

        if neg:
            doc_ids = [ i for i in range(len(self.documents))
                          if i not in doc_ids ]

        return doc_ids


    def answer_bool(self, query):
        """ Answers a query given in cnf form.
            Input:
                query: String containing the query of the user in conjuctive normal form.
            Output:
                doc_ids: A set containing the docIds of the resulting documents
        """
        or_operator = '|'
        and_operator = '&'

        clauses = query.split(and_operator)
        or_terms = clauses[0].split(or_operator)

        doc_ids = set()
        for term in or_terms:
            try:
                doc_ids.update(self.answer(term))
            except KeyError:
                pass

        n = len(clauses)
        for i in range(1, n):
            or_terms = clauses[i].split(or_operator)

            clause_ids = set()

            for term in or_terms:
                try:
                    clause_ids.update(self.answer(term))
                except KeyError:
                    pass

            doc_ids = doc_ids.intersection(clause_ids)

        return doc_ids


    def print_help(self, commands):
        padding = max( list(map(lambda x: len(x), commands.keys())) )
        print ("\n< Help >")
        for k, v in commands.items():
            print (k + " " * (padding + 2 - len(k)) + "-", v)


    def print_results(self, results_docids):
        print ("\n< Results >")
        if not results_docids:
            print ("No documents found!")
        else:
            for id in results_docids:
                # print id for debugging purposes
                print (id, self.documents[id])


    def cli(self):
        commands = {
            "Exit": ";;",
            "Index": ";;index",
            "Docid": ";;docid",
            "Help": ";;help"
        }

        print("Type ;;help for more commands.")

        try:
            query = input("\nSearch: ")
        except EOFError:
            print ()
            query = commands["Exit"]

        while query != commands["Exit"]:
            if query[:2] == ";;":
                if query == commands["Help"]:
                    self.print_help(commands)
                elif query == commands["Index"]:
                    self.print_inverted_index()
                elif query == commands["Docid"]:
                    self.print_docIds()
                else:
                    print ("Invalid command.")
            else:
                results_docids = self.answer_bool(query)
                self.print_results(results_docids)

            try:
                query = input("\nSearch: ")
            except EOFError:
                print ()
                query = commands["Exit"]


def main():
    from os import sep
    import sys


    if "-d" in sys.argv:
        collection = sys.argv[sys.argv.index("-d") + 1]
        if collection[-1] == sep:
            n = len(collection) - 1
            collection = collection[:n]
    else:
        collection = "."

    if "-rf" in sys.argv:
        a = True
    else:
        a = False

    engine = BooleanEngine(collection, excluded = [], rf = a)

    engine.cli()


if __name__ == '__main__':
    main()
