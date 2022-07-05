import corpus_structure
import grammar_structure
import math

class Query:
    def __init__(self,properties,amounts,additional_rules,type_of_first_word,label):
        self.properties=properties
        self.amounts=amounts
        self.additional_rules=additional_rules
        self.type_of_first_word=type_of_first_word
        self.label=label

class QueryGraph:
    def __init__(self):
        self.colocs={}
        self.tags= {}
        self.whole_coloc_amount = {}
        self.whole_coloc_example={}
        self.beginning_amount = {}
        self.end_amount = {}
    def add(self,words,lemmas,amount, main_word_tag):
        if lemmas[0] not in self.tags.keys():
            self.tags[lemmas[0]]=[]
        if main_word_tag not in self.tags[lemmas[0]]:
            self.tags[lemmas[0]].append(main_word_tag)
        if len(lemmas)==2:
            if (lemmas[0],main_word_tag) in self.beginning_amount.keys():
                self.beginning_amount[(lemmas[0],main_word_tag)]=self.beginning_amount[(lemmas[0],main_word_tag)]+amount
            else:
                self.beginning_amount[(lemmas[0],main_word_tag)]=amount

            if lemmas[1] in self.end_amount.keys():
                self.end_amount[lemmas[1]]=self.end_amount[lemmas[1]]+amount
            else:
                self.end_amount[lemmas[1]]=amount

            if (lemmas,main_word_tag) in self.whole_coloc_amount.keys():
                self.whole_coloc_amount[(lemmas,main_word_tag)]=self.whole_coloc_amount[(lemmas,main_word_tag)]+amount
            else:
                self.whole_coloc_amount[(lemmas,main_word_tag)]=amount
                self.whole_coloc_example[(lemmas,main_word_tag)]=words
                if (lemmas[0],main_word_tag) not in self.colocs.keys():
                    self.colocs[(lemmas[0],main_word_tag)]=[]
                self.colocs[(lemmas[0],main_word_tag)].append(lemmas[1])

    def join(self,other):
        for i in other.whole_coloc_amount.keys():
            self.add(other.whole_coloc_example[i],i[0],other.whole_coloc_amount[i],i[1])

    def writeout(self,name,amount,lemma,main_word_tag):
        logDice={}
        if (lemma,main_word_tag) in self.colocs.keys():
            print(name.replace("%w",lemma))
            print("---------------------------------")
            for lemma2 in self.colocs[(lemma,main_word_tag)]:
                x=2*self.whole_coloc_amount[((lemma,lemma2),main_word_tag)]/(self.beginning_amount[(lemma,main_word_tag)]+self.end_amount[lemma2])
                y=math.log(x,2)+14
                logDice[lemma2]=y

            for i in sorted(logDice, key=logDice.get, reverse=True):
                print(i)
                print(self.whole_coloc_example[((lemma,i),main_word_tag)])
                print("---------------------------------")
                amount = amount - 1
                if amount == 0:
                    break
            print()

    def writeout_common_collocations(self,name,amount,lemma1,lemma2,main_word_tag):
        logDice = {}
        logDice2 = {}
        if (lemma1,main_word_tag) in self.colocs.keys() and (lemma2,main_word_tag) in self.colocs.keys():
            print(name.replace("%w",lemma1+"/"+lemma2))
            for lemma in self.colocs[(lemma2,main_word_tag)]:
                x=2*self.whole_coloc_amount[((lemma2,lemma),main_word_tag)]/(self.beginning_amount[(lemma2,main_word_tag)]+self.end_amount[lemma])
                y=math.log(x,2)+14
                logDice[lemma]=y

            for lemma in self.colocs[(lemma1,main_word_tag)]:
                x=2*self.whole_coloc_amount[((lemma1,lemma),main_word_tag)]/(self.beginning_amount[(lemma1,main_word_tag)]+self.end_amount[lemma])
                y=math.log(x,2)+14
                if lemma in logDice.keys():
                    logDice2[lemma]=y

            for i in sorted(logDice2, key=logDice2.get, reverse=True):
                print(i)
                print("---------------------------------")
                amount = amount - 1
                if amount == 0:
                    break
            print()



class GrammarGraph(dict):
    def __init__(self, *arg, **kw):
        super(GrammarGraph, self).__init__(*arg, **kw)

    def writeout(self,amount,lemma): #wypisanie wszystkiego
        tags=[]
        for col in self:
            if lemma in self[col].tags.keys():
                tags_here=self[col].tags[lemma]
                for tag in tags_here:
                    if tag not in tags:
                        tags.append(tag)
        for tag in tags:
            if tag!="":
                print(lemma+" as "+tag+":")
            for col in self:
                self.write_one(col,amount,lemma,tag)

    def give_keys(self):
        return [col for col in self]

    def write_one(self, col,amount,lemma,tag): #wypisanie konkretnej kolokacji
        self[col].writeout(col,amount,lemma,tag)

    def common_collocations(self, amount, lemma1, lemma2):
        tags = []
        for col in self:
            if lemma1 in self[col].tags.keys():
                tags_here = self[col].tags[lemma1]
                for tag in tags_here:
                    if tag not in tags:
                        tags.append(tag)
        tags2 = []
        for col in self:
            if lemma2 in self[col].tags.keys():
                tags_here = self[col].tags[lemma2]
                for tag in tags_here:
                    if tag not in tags2:
                        tags2.append(tag)
        for tag in tags:
            if tag != "" and tag in tags2:
                print(lemma1 + " as " + tag + ":")
            for col in self:
                self[col].writeout_common_collocations(col,amount,lemma1,lemma2,tag)

    def join(self,other):
        for col in other:
            self[col].join(other[col])

