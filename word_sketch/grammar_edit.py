import sys

def add_tags(line):
    opened=False
    bad=False
    line2=""
    for i in range(len(line)):
        if line[i] == '"' and opened == False:
            opened = True
            if i==0 or (line[i-1]!="=" and not (line[i-1]==' ' and line [i-2]=='=')):
                bad=True
                if line[i-2:i]!='"|':
                    line2=line2+"[tag="
                else:
                    line2=line2+"tag="
            line2=line2+line[i]
        elif line[i]=='"' and opened==True:
            opened=False
            line2=line2+line[i]
            if bad==True:
                bad=False
                if line[i+1:i+3]!='|"':
                    line2=line2+"]"
        else:
            if not (line[i]==" "and (line[i+1]=="=" or line[i-1]=="=")):
                line2=line2+line[i]
    return line2


def better_ors(line):
    word=False
    tag=False
    lemma=False
    opened=False
    cuts=[]
    cuts.append(0)
    for i in range(len(line)):
        if line[i]=='"' and opened==False:
            opened=True
            if i>=4:
                if line[i-4:i]=="tag=":
                    tag=True
            if i>=6:
                if line[i-6:i]=="lemma=":
                    lemma=True
            if i>=5:
                if line[i-5:i]=="word=":
                    word=True
        elif line[i]=='"' and opened==True:
            opened = False
            if line[i+1]!="|" and line[i+1:i+4]!="]|[":
                tag = False
                lemma = False
                word = False
            else:
                if (line[i+1:i+7] == '|tag="') and (tag or line[i+7:i+9]==',"'):
                    cuts.append(i)
                    cuts.append(i+1)
                    cuts.append(i+2)
                    cuts.append(i+7)
                elif (line[i+1:i+9] == ']|[tag="') and (tag or line[i+9:i+12]==',"]'):
                    cuts.append(i)
                    cuts.append(i+2)
                    cuts.append(i+3)
                    cuts.append(i+9)
                elif line[i+1:i+8]=='|word="' and (word or line[i+8:i+10]==',"'):
                    cuts.append(i)
                    cuts.append(i+1)
                    cuts.append(i+2)
                    cuts.append(i+8)
                elif line[i+1:i+10]==']|[word="' and (word or line[i+10:i+13]==',"]'):
                    cuts.append(i)
                    cuts.append(i+2)
                    cuts.append(i+3)
                    cuts.append(i+10)
                elif (line[i+1:i+9] == '|lemma="') and (lemma or line[i+9:i+11]==',"'):
                    cuts.append(i)
                    cuts.append(i+1)
                    cuts.append(i+2)
                    cuts.append(i+9)
                elif (line[i+1:i+11] == ']|[lemma="') and (lemma or line[i+11:i+14] == ',"]'):
                    cuts.append(i)
                    cuts.append(i+2)
                    cuts.append(i+3)
                    cuts.append(i+11)
                else:
                    opened=False
                    tag=False
                    lemma=False
                    word=False
    cuts.append(len(line))
    line2=""
    for i in range(len(cuts)):
        if i%2==0:
            line2=line2+line[cuts[i]:cuts[i+1]]
    return line2


def remove_unneeded_parenthases(line):
    how_many_parenthases_deep=0
    opening=0
    closing=0
    how_many_equals_signs=0
    where_first_equals_sign=0
    line2=""
    for i in range(len(line)):
        if how_many_parenthases_deep==0 and line[i]=='!' and line[i+1]=='(':
            skip="turn"
        elif how_many_parenthases_deep==0 and line[i]!='(':
            line2=line2+line[i]
        elif line[i]=='(':
            if how_many_parenthases_deep==0:
                opening=i
            how_many_parenthases_deep=how_many_parenthases_deep+1
        elif how_many_parenthases_deep>0 and line[i]=='=':
            how_many_equals_signs=how_many_equals_signs+1
            if where_first_equals_sign==0:
                where_first_equals_sign=i
        elif how_many_parenthases_deep>1 and line[i] == ')':
            how_many_parenthases_deep=how_many_parenthases_deep-1
        elif how_many_parenthases_deep==1 and line[i]==')':
            closing=i
            if how_many_equals_signs==1 and line[closing-1]=='"' and (line[opening+1:opening+6]=='tag="' or line[opening+1:opening+7]=='word="' or line[opening+1:opening+8]=='lemma="'):
                line2=line2+line[opening+1:where_first_equals_sign]
                if line[opening-1]=='!':
                    line2=line2+'!'
                line2=line2+line[where_first_equals_sign:closing]
            elif how_many_equals_signs==1 and line[closing-2:closing]=='"]' and (line[opening+1:opening+7]=='[tag="' or line[opening+1:opening+8]=='[word="' or line[opening+1:opening+9]=='[lemma="'):
                line2=line2+line[opening+1:where_first_equals_sign]
                if line[opening-1]=='!':
                    line2=line2+'!'
                line2=line2+line[where_first_equals_sign:closing]
            else:
                line2=line2+line[opening:closing+1]
            how_many_parenthases_deep=0
            how_many_equals_signs=0
            opening=0
            closing=0
            where_first_equals_sign=0
    return line2

def remove_spaces(line):
    line2=""
    for i in range(len(line)):
        if line[i]!=" ":
            line2=line2+line[i]
    return line2

def add_amounts(line):
    line2=""
    opened=0
    for i in range(len(line)):
        if not(line[i]=="?" and opened==0):
            line2=line2+line[i]
        if line[i]=="[": opened=opened+1
        if line[i]=="]": opened=opened-1
        if line[i]=="]" and line[i+1]!="{" and opened==0:
            if line[i+1]=="?":
                line2=line2+"{0,1}"
            else:
                line2= line2+"{1,1}"
        if line[i]==")" and opened==0 and line[i+1]=="?":
            line2 = line2 + "{0,1}"
    return line2

def move_amounts(line):
    is_extra=True
    line2=""
    extra=""

    for i in range(2, len(line) + 1):
        if line[len(line) - i] == "}":
            is_extra = False
        if is_extra == False:
            line2 = line[len(line) - i] + line2
        else:
            extra = line[len(line) - i] + extra
    line3=""
    amounts = "("
    in_amount=False
    in_parenthases=0
    for i in range(len(line2)):
        if line2[i]=="(" and in_amount==False:
            in_parenthases=in_parenthases+1
        if line2[i]==")" and in_parenthases!=0:
            in_parenthases=in_parenthases-1
        if line2[i]=="{" and in_parenthases==0 and (line2[i-1]=="]" or line2[i-1]==")"):
            in_amount=True
        if in_amount:
            amounts=amounts+line2[i]
            if line2[i]=="}":
                in_amount=False
        else:
            line3=line3+line2[i]
    amounts=amounts+")"


    return line3+amounts+extra+"\n"


def edit_grammar(path_in,path_out):
    input=open(path_in,"r")
    output=open(path_out,"w")
    for line in input:
        if line[0] != "#" and line[0] != "=" and line[0] != "*" and line[0] != "\n":
            line2=remove_spaces(line)
            line3=add_tags(line2)
            line4 = better_ors(line3)
            line5 = remove_unneeded_parenthases(line4)
            line6= add_amounts(line5)
            line7= move_amounts(line6)
            output.write(line7)
        else:
            output.write(line)
    output.close()
    input.close()