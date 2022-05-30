import cqls

import grammar_structure
import grammar_edit

class Collocation:      #ta funkcja przechowuje kolokację. Zapisuje jej nazwę, wszystkie wyszukiwania które pozwalają znaleźć
                        #jej występowania, i label który w tych wyszukiwaniach ma słowo podawane w zapytaniu.
    def __init__(self, name, main_label, queries):
        self.name=name
        self.main_label=main_label
        self.queries=queries

    def search(self,lemma,corpus):      #ta funkcja wykonuje wszystkie wyszukiwania zapisane w kolokacji, i łączy ich wyniki w jeden
                                        #duży wynik wyszukiwania całej kolokacji
        big_query=corpus.search(self.queries[0],lemma,self.main_label)
        for i in range(1,len(self.queries)):
            big_query.join(corpus.search(self.queries[i],lemma,self.main_label))
        return big_query

    def add(self,query):
        self.queries.append(query)

    def writeout(self):
        print(self.name)
        print("Main Label: "+str(self.main_label))
        print("Queries:")
        for i in self.queries:
            print(i.properties)
        print()

class Query:
    def __init__(self,properties,amounts,additional_rules):
        self.properties=properties
        self.amounts=amounts
        self.rules=additional_rules


class Grammar:
    def __init__(self):
        self.order=[] #order to kolejność w której mamy wypisywać kolokacje, podana w pliku gramatyki powierzchniowej
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

    def find(self, lemma,corpus):   #to funkcja która wyszukuje wszystkie zadane w gramatyce kolokacje danej lemmy w danym korpusie
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
class Amount:
    def __init__(self,min,max):
        self.min=min
        self.max=max
    def writeout(self):
        print("{"+str(self.min)+","+str(self.max)+"}")

def parse_amounts(amounts):
    parsed_amounts=[]
    for i in range(len(amounts)):
        if amounts[i]==",":
            amount= Amount(int(amounts[i-1]),int(amounts[i+1]))
            parsed_amounts.append(amount)
    return parsed_amounts

def parse_properties(line):
    properties=[]
    bit=""
    in_parenthases=0
    in_brackets=0
    for i in range(len(line)):
        bit=bit+line[i]
        if in_parenthases==0 and in_brackets==0:
            if line[i]=="[":
                in_brackets=1
            elif line[i]=="(":
                in_parenthases=1
            elif line[i]=="*":
                bit=""
        else:
            if line[i]=="[" and in_brackets!=0:
                in_brackets=in_brackets+1
            if line[i]=="]" and in_brackets!=0:
                in_brackets=in_brackets-1
                if in_brackets==0:
                    properties.append(cqls.parse(bit))
                    bit=""
            if line[i]=="(" and in_parenthases!=0:
                in_parenthases=in_parenthases+1
            if line[i]==")" and in_parenthases!=0:
                in_parenthases=in_parenthases-1
                if in_parenthases==0:
                    properties.append(cqls.parse(bit))
                    bit=""
    return properties




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
                amounts=""
                extra=""
                is_extra=True
                is_amounts=False
                for i in range(2,len(line)+1):
                    if line[len(line)-i]==")" and is_extra==True:
                        is_extra=False
                        is_amounts=True
                    if line[len(line)-i]=="]" and is_amounts==True:
                        is_amounts=False

                    if is_extra==True:
                        extra=line[len(line)-i]+extra
                    elif is_amounts==True:
                        amounts=line[len(line)-i]+amounts
                    else:
                        line2=line[len(line)-i]+line2
                amounts_parsed=parse_amounts(amounts)
                properties=parse_properties(line2)
                additional_rules=[]
                if len(properties)!=len(amounts_parsed):
                    print(len(properties))
                    print(len(amounts_parsed))
                    print(line)
                    print(properties)
                query=Query(properties,amounts_parsed,additional_rules)

                grammar.collocations[len(grammar.collocations) - 1].add(query)
                if dual or symmetric:
                    grammar.collocations[len(grammar.collocations)-2].add(query)
    return grammar




