import re
import sys
from bs4 import BeautifulSoup
import grammar_structure
import math
import query_structure

'''
An object of this class holds information about a word in a corpus, its' lemma and tag, and allows for useful functions.
'''
class Word:
    #dashes_in_lemmas is necessary because some corpora hold information in a format "word lemma-tag tag", and we
    #need to separate lemmas from tags in those cases
    def __init__(self, line, dashes_in_lemmas):
        first_gap=int(line.find("\t",0,-1))
        word=line[0:first_gap]
        second_gap=line.find("\t",first_gap+1,-1)
        tag=line[first_gap+1:second_gap]
        lemma = line[second_gap + 1:]
        self.word=word.lower()
        self.tag = tag
        if len(lemma)!=0:
            if lemma[-1]=="\n":
                lemma=lemma[0:-1]
        if dashes_in_lemmas:
            if lemma.find("-")!=-1:
                lemma=lemma[0:lemma.find("-")]
        self.lemma=lemma.lower()


    def writeout(self):
        print("word="+self.word+";")
        print("tag="+self.tag+";")
        print("lemma="+self.lemma+";")

    def equals(self,other):
        if self.word==other.word:
            return True
        else:
            return False

    def same_lemma(self,other):
        if self.lemma==other.lemma:
            return True
        else:
            return False

    def match(self, property):
        if "match" in property.keys():
            for key in property["match"].keys():
                if "word"==key:
                    for i in property["match"]["word"]:
                        if not re.fullmatch(i, self.word):
                                return False
                elif "tag"==key:
                    for i in property["match"]["tag"]:
                        if not re.fullmatch(i, self.tag):
                            return False
                elif "lemma"==key:
                    for i in property["match"]["lemma"]:
                        if not re.fullmatch(i, self.lemma):
                            return False
        if "not_match" in property.keys():
            for key in property["not_match"].keys():
                if "word"==key:
                    for i in property["not_match"]["word"]:
                        if re.fullmatch(i, self.word):
                            return False
                elif "tag"==key:
                    for i in property["not_match"]["tag"]:
                        if re.fullmatch(i, self.tag):
                            return False
                elif "lemma"==key:
                    for i in property["not_match"]["lemma"]:
                        if re.fullmatch(i, self.lemma):
                            return False
        return True


def transform_xml_line(root):
    #extract from tags
    word = root.find("orth")
    pom = root.find("lex")
    tag = pom.find("ctag")
    lemma = pom.find("base")
    #drop tags
    w = str(re.search('<[a-z]{4}>(.*?)</[a-z]{4}>', str(word)).group(1))
    t = str(re.search('<[a-z]{4}>(.*?)</[a-z]{4}>', str(tag)).group(1))
    l = str(re.search('<[a-z]{4}>(.*?)</[a-z]{4}>', str(lemma)).group(1))

    final = w + "	" + t + "	" + l
    return final

'''
An object of this function holds information about all of the words in a corpus, as well as where the words that
might be a start of a phrase that is the answer to a query are located. For example, if there are queries that have 
a noun at the start, one of the types[] will be a list of all of the locations of nouns in the corpus.
'''
class Corpus:
    def __init__(self,path,grammar,KPWr=False):
        self.words=[]
        self.types=[]
        self.types.append([])
        for i in grammar.first_word_types.keys():
            self.types.append([])
        if KPWr:
            with open(path, 'r', encoding="utf-8") as f:
                # read and parse data
                data = f.read()
                Bs_data = BeautifulSoup(data, "xml")
                tokens = Bs_data.find_all('tok')
                word_num = 0
                for t in tokens:
                    res = transform_xml_line(t)
                    self.words.append(Word(res,False))
                    self.types[0].append(word_num)
                    for i in grammar.first_word_types.keys():
                        if Word(res, False).match(grammar.first_word_types[i]):
                            self.types[i].append(word_num)
                    word_num = word_num + 1
        else:
            input=open(path,"r",encoding="UTF-8")
            word_num=0
            x = 0
            dashes_in_lemmas=True
            for n in input:
                if n[0] != "<":
                    x=x+1
                    if x==100:
                        break
                    if n.find("-")==-1:
                        dashes_in_lemmas=False
            for n in input:
                if n[0]!="<":
                    self.words.append(Word(n,dashes_in_lemmas))
                    self.types[0].append(word_num)
                    for i in grammar.first_word_types.keys():
                        if Word(n,dashes_in_lemmas).match(grammar.first_word_types[i]):
                            self.types[i].append(word_num)
                    word_num=word_num+1
            input.close()

    def writeout(self):
        for w in self.words:
            w.writeout()

    def writeout_a_part(self,amount):
        x=0
        for w in self.words:
            w.writeout()
            x=x+1
            if x==amount:
                break

    def writeout_types(self):
        for i in range(len(self.types)):
            print(i)
            for j in range(0,min(25,len(self.types[i]))):
                self.words[self.types[i][j]].writeout()

    # This function searches through all of the corpus for the results of a query, and returns a QueryGraph with
    #those results.
    def search(self, query):
        results=query_structure.QueryGraph()
        properties = query.properties
        amounts = query.amounts
        additional_rules=query.additional_rules
        label=query.label
        x=0
        for j in self.types[query.type_of_first_word]:
            example = ""
            words = {}
            self.check_here(properties, amounts,additional_rules, 0, amounts[0].min, amounts[0].max, j, label,example, words, results)
        return results

    #This function checks whether the words in a place specified in corpus can fulfill the query with the attributes
    #specified in it.
    def check_here(self,properties,amounts,additional_rules,place_in_properties,min,max,place_in_corpus,searched_label,example,words,results):
        if len(self.words)>place_in_corpus+1:
            if min==0:
                if len(properties) <= place_in_properties+1:
                    fulfills_additional_rules=True
                    if additional_rules!="":
                        if additional_rules=="1.tag=2.tag" or "2.tag=1.tag":
                            fulfills_additional_rules=(words[1].tag==words[2].tag)
                        elif additional_rules=="1.tag!=2.tag" or "2.tag!=1.tag":
                            fulfills_additional_rules=(words[1].tag!=words[2].tag)

                        elif additional_rules=="1.tag=3.tag" or "3.tag=1.tag":
                            fulfills_additional_rules=(words[1].tag==words[3].tag)
                        elif additional_rules=="1.tag!=3.tag" or "3.tag!=1.tag":
                            fulfills_additional_rules=(words[1].tag!=words[3].tag)

                        elif additional_rules=="3.tag=2.tag" or "2.tag=3.tag":
                            fulfills_additional_rules=(words[3].tag==words[2].tag)
                        elif additional_rules=="3.tag!=2.tag" or "2.tag!=3.tag":
                            fulfills_additional_rules=(words[3].tag!=words[2].tag)

                        else:
                            print("I can't interpret "+additional_rules+". I will ignore that part of the query.")

                    if fulfills_additional_rules:
                        lemmas=[]
                        lemmas.append(words[int(searched_label)].lemma)
                        tag=words[int(searched_label)].tag
                        main_word_tag = ""
                        if re.fullmatch("N.*[^Z]",tag):
                            main_word_tag="noun"
                        elif re.fullmatch("JJ.*",tag):
                            main_word_tag="adjective"
                        if re.fullmatch("V.*",tag):
                            main_word_tag="verb"
                        if re.fullmatch("RB.*",tag):
                            main_word_tag="adverb"
                        for i in range(len(words)):
                            if i+1!=int(searched_label):
                                lemmas.append(words[i+1].lemma)
                        results.add(example, tuple(lemmas), 1, main_word_tag)
                else:
                    self.check_here(properties, amounts,additional_rules,place_in_properties+1,amounts[place_in_properties+1].min, amounts[place_in_properties+1].max,place_in_corpus,searched_label,example,words,results)
                if max>0:
                    self.check_here(properties,amounts,additional_rules,place_in_properties,1,max,place_in_corpus,searched_label,example,words,results)
            else:
                if len(properties[place_in_properties][0])==1:
                    if self.words[place_in_corpus].match(properties[place_in_properties][0][0]):
                        if "__label__" in properties[place_in_properties][0][0].keys():
                            a=properties[place_in_properties][0][0]["__label__"][0]
                            words[int(a)]=self.words[place_in_corpus]
                            if a==str(searched_label):
                                example = example + " "+"\033[1m" + self.words[place_in_corpus].word+'\033[0m'
                                self.check_here(properties, amounts,additional_rules,place_in_properties,min-1,max-1, place_in_corpus + 1, searched_label,example,words, results)
                            else:
                                example = example + " " + self.words[place_in_corpus].word
                                self.check_here(properties, amounts,additional_rules,place_in_properties,min-1,max-1, place_in_corpus + 1,searched_label,example,words, results)
                        else:
                            if len(example)>1 and example[-1]!=".":
                                example=example+(" ...")
                            self.check_here(properties,amounts,additional_rules,place_in_properties,min-1,max-1,place_in_corpus+1,searched_label,example,words,results)
                else:
                    match=True
                    for i in range(len(properties[place_in_properties][0])):
                        if not self.words[place_in_corpus+i].match(properties[place_in_properties][0][i]):
                            match=False
                    if match:
                        if len(example) > 1 and example[-1] != ".":
                            example=example+(" ...")
                        self.check_here(properties,amounts,additional_rules,place_in_properties,min-1,max-1,place_in_corpus+len(properties[place_in_properties][0]),searched_label,example,words,results)
