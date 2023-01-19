import cqls
from tqdm import tqdm

from .grammar_edit import edit_grammar
from .query_structure import Query

'''
An object of this class holds information about the name of a collocation type, and about every query
that comprises it. It allows for searching through all of the corpus for all of the phrases that fit
one of those queries.
'''
class Collocation:
    def __init__(self, name, queries):
        self.name=name
        self.queries=queries

    def search(self,corpus):
        big_query = corpus.search(self.queries[0])
        for i in range(1, len(self.queries)):
            big_query.join(corpus.search(self.queries[i]))
        return big_query

    def add(self,query):
        self.queries.append(query)

    def writeout(self):
        print(self.name)
        print("Queries:")
        for i in self.queries:
            print(i.label)
            print(i.type_of_first_word)
            print(i.properties)
        print()

'''
An object of this class holds information about every collocation that comprises a sketch grammar, and 
the order that the information about them should be returned in.
'''
class Grammar:
    def __init__(self):
        self.order=[]
        self.collocations=[]
        self.first_word_types={}

    def writeout(self):
        if self.order==[]:
            for j in self.collocations:
                j.writeout()
        else:
            for i in self.order:
                for j in self.collocations:
                    if j.name==i:
                        j.writeout()

    def find_all(self, corpus):
        print("Searching for collocations:")
        sketch = {}
        how_many_collocations = len(self.collocations)
        if self.order == []:
            for j in tqdm(self.collocations,total=how_many_collocations):
                result = j.search(corpus)
                if len(result.whole_coloc_amount) > 0:
                    sketch[j.name] = result
        else:
            for i in tqdm(self.order,total=how_many_collocations):
                for j in self.collocations:
                    if j.name == i:
                        result = j.search(corpus)
                        if len(result.whole_coloc_amount) > 0:
                            sketch[j.name] = result
        return sketch


'''
This function parses information about the properties, the first part of a sketch grammar line that was edited
by grammar_edit.edit_grammar. For more information, see query_structure.
'''
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

'''
This function parses information about the amounts, the second part of a sketch grammar line that was edited
by grammar_edit.edit_grammar. For more information, see query_structure.
'''
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

'''
This function parses information about the additional rules, the third part of a sketch grammar line that was edited
by grammar_edit.edit_grammar. For more information, see query_structure.
'''
def parse_extra(extra):
    additional_rules=""
    if extra != "":
        additional_rules=extra[1:]
    return additional_rules


'''
This function takes in a sketch grammar file, parses it, and returns a Grammar object that contains the grammar
described in it.
'''
def read_grammar_file(path):
    edit_grammar(path,"word_sketch/files/tmp/grammar_out.txt")
    grammar_file=open("word_sketch/files/tmp/grammar_out.txt")
    grammar=Grammar()
    dual=False
    symmetric=False
    where_is_1=-1
    where_is_2=-1
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
                    add1=True
                    add2=True
                    for x in range(len(grammar.collocations)):
                        if grammar.collocations[x].name==name1:
                            add1=False
                            where_is_1=x
                        if grammar.collocations[x].name==name2:
                            add2=False
                            where_is_2=x
                    if add1:
                        grammar.collocations.append(Collocation(name1,[]))
                        where_is_1=len(grammar.collocations)-1
                    if add2:
                        grammar.collocations.append(Collocation(name2, []))
                        where_is_2=len(grammar.collocations)-1
                else:
                    name=""
                    for i in range(1,len(line)-1):
                        name=name+line[i]
                    grammar.collocations.append(Collocation(name,[]))
                    where_is_1 = len(grammar.collocations) - 1
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
                additional_rules=parse_extra(extra)
                if amounts_parsed[0].min>0:
                    type={}
                    if "match" in properties[0][0][0].keys():
                        type["match"]=properties[0][0][0]["match"]
                    else:
                        type["match"]={}
                    if "not_match" in properties[0][0][0].keys():
                        type["not_match"] = properties[0][0][0]["not_match"]
                    else:
                        type["match"]={}
                    matched=False
                    for word_type in grammar.first_word_types.keys():
                        if matched==False and grammar.first_word_types[word_type]["match"]==type["match"] and grammar.first_word_types[word_type]["not_match"]==type["not_match"]:
                            type_of_first_word=word_type
                            matched=True
                    if matched==False:
                        type_of_first_word = len(grammar.first_word_types)+1
                        grammar.first_word_types[type_of_first_word]=type
                else:
                    type_of_first_word = 0

                query=Query(properties,amounts_parsed,additional_rules,type_of_first_word,1)
                query2=Query(properties,amounts_parsed,additional_rules,type_of_first_word,2)

                if symmetric:
                    grammar.collocations[where_is_1].add(query)
                    grammar.collocations[where_is_1].add(query2)
                elif dual:
                    grammar.collocations[where_is_1].add(query)
                    grammar.collocations[where_is_2].add(query2)
                else:
                    grammar.collocations[where_is_1].add(query)
    return grammar




