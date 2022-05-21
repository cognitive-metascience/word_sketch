import regex

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

    def match(self, attributes):
        match=True
        if "match" in attributes.keys():
            match_keys=attributes["match"].keys()
            if "word" in match_keys:
                for i in attributes["match"]["word"]:
                    if not regex.fullmatch(i, self.word):
                            match=False
            if "tag" in match_keys:
                for i in attributes["match"]["tag"]:
                    if not regex.fullmatch(i, self.tag):
                        match=False
            if "lemma" in match_keys:
                for i in attributes["match"]["lemma"]:
                    if not regex.fullmatch(i, self.lemma):
                        match=False
        if "not_match" in attributes.keys():
            not_match_keys = attributes["not_match"].keys()
            if "word" in not_match_keys:
                for i in attributes["not_match"]["word"]:
                    if regex.fullmatch(i, self.word):
                        match=False
            if "tag" in not_match_keys:
                for i in attributes["not_match"]["tag"]:
                    if regex.fullmatch(i, self.tag):
                        match=False
            if "lemma" in not_match_keys:
                for i in attributes["not_match"]["lemma"]:
                    if regex.fullmatch(i, self.lemma):
                        match=False
        return match


class WordSet:
    def __init__(self,label):
        self.words = {}
        self.order=[]
        self.label=label

    def equals(self,other):
        if self.words.keys()==other.words.keys():
            result=True
            for i in self.words.keys():
                if not self.words[i].equals(other.words[i]):
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
                if self.words[str(i)].word!="'s":
                    sentence = sentence + " "
                sentence=sentence+'\033[1m'+ self.words[str(i)].word+'\033[0m'
            else:
                sentence=sentence+" "+self.words[str(i)].word
        print(sentence)

class ColocSet:
    def __init__(self):
        self.colocs = {}
    def add(self,wordset,amount):
        add=True
        for i in self.colocs.keys():
            if wordset.equals(i) and add==True:
                self.colocs[i]=self.colocs[i]+amount
                add=False
        if add==True:
            self.colocs[wordset]=amount

    def join(self,other):
        for i in other.colocs.keys():
            self.add(i,other.colocs[i])

    def writeout(self):
        for i in self.colocs.keys():
            print("Amount: "+str(self.colocs[i]))
            i.writeout()




class Corpus:
    def __init__(self,path):
        self.words=[]
        input=open(path,"r",encoding="UTF-8")
        for n in input:
            if n[0]!="<":
                self.words.append(Word(n))

    def search(self,queries,searched_lemma,searched_label):
        results=ColocSet()
        for i in range(len(queries)):
            query=queries[i]
            for j in range(len(self.words)-len(query)):
                correct=True
                result=WordSet(searched_label)
                for k in range(len(query)):
                    if correct==True:
                        if not self.words[j+k].match(query[k]):
                            correct=False
                        elif "__label__" in query[k].keys():
                            label=(query[k]["__label__"][0])
                            result.words[label]=self.words[j+k]
                            result.order.append(label)
                            if label==str(searched_label) and self.words[j+k].lemma!=searched_lemma:
                                correct=False
                        else:
                            if len(result.order)==1:
                                result.order.append("...")
                if correct==True:
                    results.add(result,1)
        return results

