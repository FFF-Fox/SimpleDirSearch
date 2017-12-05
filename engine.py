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
                                                or ex == dirpath
                                                or ex == filename
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


    def build_inverted_index(self):
        """ Build the inverted index from the documents in the collection. """
        # Fill the index with all the appearences of each term in every
        # document.
        for i, doc in enumerate(self.documents):
            doc_contents = self.file_contents_of(doc)

            terms = self.terms_of(doc_contents)

            for term in terms:
                if (term not in self.inverted_index):
                    self.inverted_index[term] = [i]
                else:
                    self.inverted_index[term].append(i)

        # Merge the appearences, create the posting list and sort
        # it based on docId.
        for term in self.inverted_index:
            C = Counter(self.inverted_index[term])
            self.inverted_index[term] = [(i, C[i]) for i in C]
            self.inverted_index[term].sort()


    def build_index_from(self, collection_path, excluded=[], rf=True):
        """ Build the inverted index from the given collection path. """
        self.make_doclist_from(collection_path, excluded, rf)
        self.build_inverted_index()


    def print_inverted_index(self):
        """ Prints the inverted index in an easy for the eye form. """
        terms = self.inverted_index.keys()
        L = max( list(map(lambda x: len(x), terms)) )
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


def main():
    collection_path = '../../WebDevelopment/NodeTutorials/ExpressTutorial/crood/views'

    ex = ["cookie.ejs", collection_path + '/index.ejs', 'templates', 'blog.ejs', 'createpost']

    engine = Engine(collection_path, excluded = ex)
    for doc in engine.documents:
        print (doc)

    engine.print_inverted_index()
    engine.print_docIds()


if __name__ == '__main__':
    main()
