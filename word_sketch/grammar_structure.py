import re
from bs4 import BeautifulSoup
import grammar_import


class Word:
    def __init__(self, line):
        word=""
        tag=""
        lemma=""
        which_part=0
        lemma_cutoff=False
        for i in range(len(line)):
            if line[i]=="\t":
                which_part=which_part+1
            else:
                if which_part==0:
                    word=word+line[i]
                elif which_part==1:
                    tag=tag+line[i]
                elif which_part==2:
                    if line[i]=="-":
                        lemma_cutoff=True
                    else:
                        if lemma_cutoff==False:
                            lemma=lemma+line[i]
        self.word=word.lower()
        self.tag = tag
        self.lemma=lemma


    def writeout(self):
        print(self.word)
        print("tag= "+self.tag)
        print("lemma= "+self.lemma)

    def equals(self,other):
        if self.word==other.word:
            return True
        else:
            return False

    def match(self, attribute): #ta funkcja sprawdza czy dane słowo spełnia warunki zapisane w gramatyce, w formacie jsonowym
                                #{"match":{"tag":{...},"word":{...},lemma:{...}},"not_match":{"tag":{...},"word":{...},lemma:{...}}}
        match=True
        if "match" in attribute.keys():
            match_keys=attribute["match"].keys()
            if "word" in match_keys:
                for i in attribute["match"]["word"]:
                    if not re.fullmatch(i, self.word):
                            match=False
            if "tag" in match_keys:
                for i in attribute["match"]["tag"]:
                    if not re.fullmatch(i, self.tag):
                        match=False
            if "lemma" in match_keys:
                for i in attribute["match"]["lemma"]:
                    if not re.fullmatch(i, self.lemma):
                        match=False
        if "not_match" in attribute.keys():
            not_match_keys = attribute["not_match"].keys()
            if "word" in not_match_keys:
                for i in attribute["not_match"]["word"]:
                    if re.fullmatch(i, self.word):
                        match=False
            if "tag" in not_match_keys:
                for i in attribute["not_match"]["tag"]:
                    if re.fullmatch(i, self.tag):
                        match=False
            if "lemma" in not_match_keys:
                for i in attribute["not_match"]["lemma"]:
                    if re.fullmatch(i, self.lemma):
                        match=False
        return match


class Coloc:                #ten obiekt zapisuje informacje o jednej kolokacji: jakie słowa zawierała, w jakiej kolejności były
                            #ułożone, i które z nich było zadane w wyszukiwaniu (label) a które są wynikami wyszukiwania.
    def __init__(self,label):
        self.words = {}
        self.order=[]
        self.label=label

    def clone(self):
        clone= Coloc(self.label)
        clone.words=self.words.copy()
        clone.order=self.order.copy()
        return clone

    def equals(self,other):
        if self.words.keys()==other.words.keys() and self.label==other.label:
            result=True
            for i in self.words.keys():
                if self.words[i]!=other.words[i]:
                    result=False
            return result
        else:
            return False

    def writeout(self):
        sentence=""
        for i in self.order:
            if i=="...":
                sentence=sentence+" ..."
            elif str(i)!=str(self.label):
                if self.words[str(i)]!="'s":
                    sentence = sentence + " "
                sentence=sentence+'\033[1m'+ self.words[str(i)]+'\033[0m'
            else:
                sentence=sentence+" "+self.words[str(i)]
        print(sentence)

class ColocSet:     #ten obiekt zawiera informację o wszystkich kolokacjach będących wynikami danego wyszukiwania, pod postacią słownika,
                    #gdzie każdej kolokacji przypisuję ilość jej wystąpień.
    def __init__(self):
        self.colocs = {}
    def add(self,coloc,amount):
        add=True
        for i in self.colocs.keys():
            if coloc.equals(i) and add==True:
                self.colocs[i]=self.colocs[i]+amount
                add=False
        if add==True:
            self.colocs[coloc]=amount

    def join(self,other):
        for i in other.colocs.keys():
            self.add(i,other.colocs[i])

    def writeout(self):
        for i in self.colocs.keys():
            print("Amount: "+str(self.colocs[i]))
            i.writeout()


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


class Corpus:
    def __init__(self,path,KPWr=False):
        self.words=[]
        if KPWr:
            with open(path, 'r', encoding="utf-8") as f:
                # read and parse data
                data = f.read()
                Bs_data = BeautifulSoup(data, "xml")
                tokens = Bs_data.find_all('tok')
                for t in tokens:
                    res = transform_xml_line(t)
                    self.words.append(Word(res))
        else:
            input=open(path,"r",encoding="UTF-8")
            for n in input:
                if n[0]!="<":
                    self.words.append(Word(n))

    def writeout(self):
        for w in self.words:
            w.writeout()

    def search(self,query,searched_lemma,searched_label):
        results=ColocSet()
        attributes=query.properties
        amounts=query.amounts
        for j in range(len(self.words)):
            result= Coloc(searched_label)
            self.check_here(attributes,amounts,j,searched_lemma,searched_label,result.clone(),results)
        return results

    def check_here(self,attributes,amounts,place,searched_lemma,searched_label,result,results):
        if len(attributes)==0:
            results.add(result,1)
        elif len(self.words)>place+1:
            if amounts[0].min==0:
                attributes1=attributes.copy()
                amounts1=amounts.copy()
                attributes1.pop(0)
                amounts1.pop(0)
                self.check_here(attributes1, amounts1,place,searched_lemma,searched_label,result.clone(),results)
                if amounts[0].max>0:
                    attributes2=attributes.copy()
                    amounts2=amounts.copy()
                    amounts2.pop(0)
                    amounts2.insert(0,grammar_import.Amount(1,amounts[0].max))
                    self.check_here(attributes2,amounts2,place,searched_lemma,searched_label,result.clone(),results)
            else:
                if len(attributes[0][0])==1:
                    if self.words[place].match(attributes[0][0][0]):
                        attributes1 = attributes.copy()
                        amounts1 = amounts.copy()
                        if "__label__" in attributes[0][0][0].keys():
                            a=str(attributes[0][0][0]["__label__"][0])
                            result.words[a]=self.words[place].word
                            result.order.append(a)
                            if a==str(searched_label):
                                if self.words[place].lemma==searched_lemma:
                                    amounts1.pop(0)
                                    amounts1.insert(0,grammar_import.Amount(amounts[0].min - 1, amounts[0].max - 1))
                                    self.check_here(attributes1, amounts1, place + 1, searched_lemma, searched_label,result.clone(), results)
                            else:
                                amounts1.pop(0)
                                amounts1.insert(0,grammar_import.Amount(amounts[0].min - 1, amounts[0].max - 1))
                                self.check_here(attributes1, amounts1, place + 1, searched_lemma, searched_label,result.clone(), results)
                        else:
                            if len(result.order)==1:
                                result.order.append("...")
                            amounts1.pop(0)
                            amounts1.insert(0,grammar_import.Amount(amounts[0].min-1,amounts[0].max-1))
                            self.check_here(attributes1,amounts1,place+1,searched_lemma,searched_label,result.clone(),results)
                else:
                    match=True
                    for i in range(len(attributes[0][0])):
                        if not self.words[place+i].match(attributes[0][0][i]):
                            match=False
                    if match:
                        attributes1 = attributes.copy()
                        amounts1 = amounts.copy()
                        if len(result.order)==1:
                            result.order.append("...")
                        amounts1.pop(0)
                        amounts1.insert(0,grammar_import.Amount(amounts[0].min-1,amounts[0].max-1))
                        self.check_here(attributes1,amounts1,place+len(attributes[0][0]),searched_lemma,searched_label,result.clone(),results)







