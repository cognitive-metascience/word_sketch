import pickle
import time

import corpus_structure
import query_structure
import grammar_structure
import treetaggerwrapper

#this function writes out 'amount' of most common collocates of 'lemma'
def search_in_parsed_corpus(path_to_parsed_corpus,lemma,amount):
    print("Searching the tagged corpus for collocates of \""+lemma+"\"")
    sketch = pickle.load(open(path_to_parsed_corpus, "rb"))
    sketch.writeout(amount, lemma)

#this function writes out 'amount' of most common collocates of 'lemma1' that are also collocates of 'lemma2'
#sketchengine does this differently, but I didn't implement that yet.
def common_collocations_in_parsed_corpus(path_to_parsed_corpus,lemma1,lemma2,amount):
    print("Searching the tagged corpus for common parts in collocates of \"" + lemma1 + "\" and \""+lemma2+"\"")
    sketch = pickle.load(open(path_to_parsed_corpus, "rb"))
    sketch.common_collocations(amount, lemma1, lemma2)

#This function reads a corpus and a sketch grammar, and finds all of the colocates of all of the
#words in that corpus, according to that sketch grammar. Then it saves the object that holds the
#data about those collocations, so that later we can access it quickly.
def parse_corpus(path_to_corpus,path_to_grammar,path_to_output):
    print("Searching the corpus for all of the collocations")
    grammar = grammar_structure.read_grammar_file(path_to_grammar)
    start=time.time()
    corpus = corpus_structure.Corpus(path_to_corpus, grammar)
    corpus_representation = query_structure.GrammarGraph(grammar.find_all(corpus))
    pickle.dump(corpus_representation, open(path_to_output, "wb"))
    end=time.time()
    print("All of the collocations found and saved in "+str((end-start)/60)[0:str((end-start)/60).find(".")]+" minutes")

#This function takes in a file containing a list of files comprising a corpus. Then it tags the
#text in those files, using Treetagger, and saves the tagged corpus in one text file.
def tag_corpus(path_to_list_of_files,path_to_output,lang):
    print("Tagging the corpus using Treetagger")
    treetaggerwrapper.TAGGER_TIMEOUT = 1000
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang, TAGDIR='C:\\TreeTagger')
    list_of_files = open(path_to_list_of_files, "r")
    tagged_corpus=open(path_to_output, "w")
    all=0
    bad=0
    for n in list_of_files:
        all=all+1
        tagger.tag_file_to(n[:-1], "output.txt")
        this_file=open("output.txt", "r")
        try:
            for line in this_file:
                tagged_corpus.write(line)
        except UnicodeDecodeError:
            bad=bad+1
        tagged_corpus.write("\n")
    print("Tagging done; tagged corpus saved.")
    if bad>0:
        print(str(bad)+"/"+str(all)+" files contained forbidden characters and could not be tagged.")