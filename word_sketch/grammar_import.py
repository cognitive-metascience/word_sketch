import cqls

import grammar_structure
import grammar_edit

class Collocation:

    def __init__(self, name, main_label, queries):
        self.name=name
        self.main_label=main_label
        self.queries=queries

    def search(self,lemma,corpus):
        big_query=corpus.search(self.queries[0].query,lemma,self.main_label)
        for i in range(1,len(self.queries)):
            big_query.join(corpus.search(self.queries[i].query,lemma,self.main_label))
        return big_query

    def add(self,query):
        self.queries.append(query)

    def writeout(self):
        print(self.name)
        print("Main Label: "+str(self.main_label))
        print("Queries:")
        for i in self.queries:
            print(i.query)
        print()

class Query:
    def __init__(self,basic_query,additional_rules):
        self.query=basic_query
        self.rules=additional_rules


class Grammar:
    def __init__(self):
        self.order=[]
        self.collocations=[]

    def writeout(self):
        if self.order==[]:
            for j in self.collocations:
                j.writeout()
        else:
            for i in self.order:
                for j in self.collocations:
                    if j.name==i:
                        j.writeout()

    def find(self, lemma,corpus):
        if self.order==[]:
            for j in self.collocations:
                result = j.search(lemma, corpus)
                if len(result.colocs)>0:
                    print()
                    print(j.name+":")
                    result.writeout()
        for i in self.order:
            for j in self.collocations:
                if j.name==i:
                    result=j.search(lemma,corpus)
                    if len(result.colocs) > 0:
                        print()
                        print(j.name+":")
                        result.writeout()


def read_grammar_file(path):
    grammar_edit.edit_grammar(path,"grammar_out.txt")
    grammar_file=open("grammar_out.txt","r")
    grammar=Grammar()
    dual=False
    symmetric=False
    for line in grammar_file:
        if line[0]!="#":
            if line.startswith("*FIXORDER"):
                option=""
                how_many=0
                for i in range(len(line)):
                    if line[i]==";" or line[i]=="\n":
                        if how_many > 0:
                            grammar.order.append(option)
                        how_many=how_many+1
                        option=""
                    else:
                        option=option+line[i]
            elif line.startswith("*SYMMETRIC"):
                symmetric=True
            elif line.startswith("*DUAL"):
                dual=True
            elif line.startswith("="):
                if dual:
                    name1=""
                    name2=""
                    second=False
                    for i in range(1,len(line)-1):
                        if line[i]=="/":
                            second=True
                        elif not second:
                            name1=name1+line[i]
                        else:
                            name2=name2+line[i]
                    grammar.collocations.append(Collocation(name1,1,[]))
                    grammar.collocations.append(Collocation(name2, 2, []))
                elif symmetric:
                    name = ""
                    for i in range(1, len(line) - 1):
                        name = name + line[i]
                    grammar.collocations.append(Collocation(name, 1, []))
                    grammar.collocations.append(Collocation(name, 2, []))
                else:
                    name=""
                    for i in range(1,len(line)-1):
                        name=name+line[i]
                    grammar.collocations.append(Collocation(name, 1, []))
            elif line=="\n":
                dual=False
                symmetric=False
            elif not line.startswith("*"):
                line2=""
                extra=""
                is_extra=True
                for i in range(2,len(line)+1):
                    if line[len(line)-i]=="]":
                        is_extra=False
                    if is_extra==False:
                        line2=line[len(line)-i]+line2
                    else:
                        extra=line[len(line)-i]+line2

                additional_rules=[]
                query=Query(cqls.parse(line2),additional_rules)
                grammar.collocations[len(grammar.collocations) - 1].add(query)
                if dual or symmetric:
                    grammar.collocations[len(grammar.collocations)-2].add(query)
    return grammar




