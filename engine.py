from os import walk
import string
from collections import Counter


class Engine:
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
            self.documents.extend([ dirpath +'/'+ filename
                                    for filename in filenames
                                    if not any( ex in dirpath.split('/')
                                                or ex == filename
                                                or ex == dirpath
                                                or ex == dirpath +'/'+ filename
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
        """ Convert the data to lowercase and strip punctuation.
            Input:
                in_string: A string.
            Output:
                out_string: The in_string converted to lowercase and stripped
                    of punctuation.
        """
        in_string = in_string.lower()

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
        for i, doc in enumerate(self.documents):
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
        # L = max( list(map(lambda x: len(x), self.documents)) )
        l = len(str(len(self.documents)))
        for i, doc in enumerate(self.documents):
            # Lpadding = " " * (L - len(doc))
            lpadding = " " * (l - len(str(i)))
            print (str(i) + lpadding + " - " + doc)


    def answer(self, query):
        """ Answer the query of the user.
            Input:
                query: String containing the query of the user.
            Output:
                doc_ids: A list containing the docIds of the resulting documents
        """
        filt_query = self.filter_string(query)

        if filt_query in self.inverted_index:
            doc_ids = self.inverted_index[filt_query]
        else:
            doc_ids = []

        return doc_ids


def main():
    collection_path = '../../WebDevelopmeent/NodeTutorials/ExpressTutorial/picoblog/views'

    ex = ["cookie.ejs", collection_path + '/index.ejs', 'templates', 'blog.ejs', 'createpost']

    engine = Engine(collection_path, excluded = ex)
    for doc in engine.documents:
        print (doc)

    # engine.add_to_index('./engine.py')
    engine.print_inverted_index()
    engine.print_docIds()
    answer_docids = engine.answer('engine')

    print ('< Answer >')
    for id in answer_docids:
        print(id, engine.documents[id])

if __name__ == '__main__':
    main()
