import pickle
import time
import nltk
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm


from .corpus_structure import Corpus
from .query_structure import GrammarGraph
from .grammar_structure import read_grammar_file

'''
This function writes out 'amount' of most common collocates of 'lemma', in every collocation type defined by
the sketch grammar. For example, if 'lemma' is "house", for the most common grammar it will write out 10 most 
common modifiers of "house", 10 most common verbs modified by "house", and so on. If a lemma can have two meanings- 
for example, "house" can be either a noun or a verb- then their collocates will be written out separately.
'''
def search_in_parsed_corpus(path_to_parsed_corpus,lemma,amount=10):
    print("Searching the tagged corpus for collocates of \""+lemma+"\"")
    sketch = pickle.load(open(path_to_parsed_corpus, "rb"))
    sketch.writeout(amount, lemma)


'''
This function writes out 'amount' of most common collocates of 'lemma1' that are also collocates of 'lemma2'
sketchengine does this differently, but that function isn't implemented here yet.
'''
def common_collocations_in_parsed_corpus(path_to_parsed_corpus,lemma1,lemma2,amount=10):
    print("Searching the tagged corpus for common parts in collocates of \"" + lemma1 + "\" and \""+lemma2+"\"")
    sketch = pickle.load(open(path_to_parsed_corpus, "rb"))
    sketch.common_collocations(amount, lemma1, lemma2)


'''
This function reads a corpus and a sketch grammar, and finds all of the colocates of all of the
words in that corpus, according to that sketch grammar. Then it saves the object that holds the
data about those collocations, so that later we can access it quickly.
'''
def parse_corpus(path_to_corpus,path_to_grammar,path_to_output,KPWr=False):
    grammar = read_grammar_file(path_to_grammar)
    start=time.time()
    corpus = Corpus(path_to_corpus, grammar, KPWr=KPWr)
    corpus_representation = GrammarGraph(grammar.find_all(corpus))
    pickle.dump(corpus_representation, open(path_to_output, "wb"))
    end=time.time()
    print("All of the collocations found and saved in "+str((end-start)/60)[0:str((end-start)/60).find(".")]+" minutes")

'''
This function takes in a text file containing a list of paths of files comprising a corpus. Then it tags the
text in those files, using nltk, and saves the tagged corpus in one text file.
'''
def tag_corpus(path_to_list_of_files,path_to_output,lang):
    print("Tagging the corpus using nltk")
    list_of_files = open(path_to_list_of_files, "r")
    tagged_corpus=open(path_to_output, "w")
    lemmatizer = WordNetLemmatizer()
    all=0
    bad=0
    how_many_files=0
    for n in list_of_files:
        how_many_files=how_many_files+1
    list_of_files.close()
    list_of_files = open(path_to_list_of_files, "r")
    for n in tqdm(list_of_files,total=how_many_files):
        all=all+1
        this_file=open(n[:-1],"r")
        try:
            text=""
            for line in this_file:
                line=line.strip()
                text=text+" "+line
                if text.find(". ")!=-1:
                    sentence=text[0:text.find(". ")+1]
                    text=text[text.find(". ")+1:]
                    tokens=nltk.tokenize.word_tokenize(sentence)
                    tags=nltk.pos_tag(tokens)
                    for tag in tags:
                        pos="n"
                        if tag[1][0]=="V":
                            pos="v"
                        if tag[1][0]=="J":
                            pos="a"
                        if tag[1][0] == "R" and tag[1][1] == "B":
                            pos = "r"
                        tagged_corpus.write(tag[0]+"\t"+tag[1]+"\t"+lemmatizer.lemmatize(tag[0],pos)+"\n")
        except UnicodeDecodeError:
            bad=bad+1
        tagged_corpus.write("\n")

    print("Tagging done; tagged corpus saved.")
    if bad>0:
        print(str(bad)+"/"+str(all)+" files contained forbidden characters and could not be tagged.")



def tag_constellate_corpus(constellate_id,path_to_output,lang):
    import constellate
    print("Tagging a constellate corpus using nltk")
    constellate.download(constellate_id, 'jsonl')
    tagged_corpus = open(path_to_output, "w")
    lemmatizer = WordNetLemmatizer()
    how_many_documents = 0
    description = constellate.get_description(constellate_id)
    how_many_documents=description['num_documents']
    for document in tqdm(constellate.dataset_reader('/root/data/'+constellate_id+'-jsonl.jsonl.gz'),total=how_many_documents):
        text=document["fullText"][0]
        sentences=nltk.tokenize.sent_tokenize(text,lang)
        for sentence in sentences:
            tokens = nltk.tokenize.word_tokenize(sentence)
            tags = nltk.pos_tag(tokens)
            for tag in tags:
                pos = "n"
                if tag[1][0] == "V":
                    pos = "v"
                if tag[1][0] == "J":
                    pos = "a"
                if tag[1][0] == "R" and tag[1][1] == "B":
                    pos = "r"
                tagged_corpus.write(tag[0] + "\t" + tag[1] + "\t" + lemmatizer.lemmatize(tag[0], pos) + "\n")