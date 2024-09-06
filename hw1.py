# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object

# ########################################

import cs547
import PorterStemmer
from cs547 import Student
import glob
import os
import re



MY_NAME = "Adina Palayoor"
MY_ANUM  = 638595108 # put your WPI numerical ID here
MY_EMAIL = "aspalayoor@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ('None', 'None')
    ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs547.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )

# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
    # Check if the directory exists first
        if not os.path.exists(base_path):
            print(f"Directory does not exist: {base_path}")
            return 0
        
        print(f"Indexing directory: {base_path}")
        num_files_indexed = 0
        
        # Check if any files are being found
        file_paths = glob.glob(os.path.join(base_path, '*.txt'))
        if not file_paths:
            print("No files found in the directory. Please check the path or the file extension.")
            return 0
        
        for file_path in file_paths:
            print(f"Processing file: {file_path}")
            try:
                # Open the file with UTF-8 encoding to avoid encoding issues
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    tokens = self.tokenize(content)
                    
                    stemmed_tokens = self.stemming(tokens)
                    
                    self._documents.append(os.path.basename(file_path))
                    doc_id = len(self._documents) - 1
                    
                    for token in stemmed_tokens:
                        if token in self._inverted_index:
                            if doc_id not in self._inverted_index[token]:
                                self._inverted_index[token].append(doc_id)
                        else:
                            self._inverted_index[token] = [doc_id]
                    
                    num_files_indexed += 1
            except UnicodeDecodeError as e:
                print(f"Error reading file {file_path}: {e}")
            
        return num_files_indexed



    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):

        text = text.lower()
        text = re.sub(r'[^a-z0-9]', ' ', text)
        tokens = text.split()
        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        stemmed_tokens = []
        stemmer = PorterStemmer.PorterStemmer()
        for token in tokens:
            stemmed_token = stemmer.stem(token, 0, len(token) - 1)
            stemmed_tokens.append(stemmed_token)
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        tokens = self.tokenize(text)
        stemmed_tokens = self.stemming(tokens)
        
        if len(stemmed_tokens) == 1:
            term = stemmed_tokens[0]
            if term in self._inverted_index:
                return [self._documents[doc_id] for doc_id in self._inverted_index[term]]
            else:
                return []
        
        elif len(stemmed_tokens) == 3:
            term1, operator, term2 = stemmed_tokens
            if operator == "and":
                if term1 in self._inverted_index and term2 in self._inverted_index:
                    result_docs = set(self._inverted_index[term1]) & set(self._inverted_index[term2])
                    return [self._documents[doc_id] for doc_id in result_docs]
            elif operator == "or":
                result_docs = set()
                if term1 in self._inverted_index:
                    result_docs |= set(self._inverted_index[term1])
                if term2 in self._inverted_index:
                    result_docs |= set(self._inverted_index[term2])
                return [self._documents[doc_id] for doc_id in result_docs]
        
        return []
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    #print(f"Indexing directory: {base_path}")
    num_files = index.index_dir('C:/Users/adina_l1uzsjt/OneDrive - Worcester Polytechnic Institute (wpi.edu)/Information Retrieval/hw1/data')
    print("indexer finished")
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

