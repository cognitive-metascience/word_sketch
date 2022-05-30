# Sketch Grammar for English, Penn Treebank tagset (TreeTagger version)
# ver. 3.3
#
# Changelog
# - Bugfix: changed PRP to PP. [13 October 2008, Jan Pomikalek]
# - Modified to allow "my" "you" etc (tag=PP$) in NPS. Looks like a typo (with
#   PRP$ not PP$) in previous version. [6 May 2008, Adam Kilgarriff]
# - Modified so that definitions don't use lempos which is not always
#   available. [Jan Pomikalek]
# - Modified to TreeTagger tagset. [Niels Ott]
# - fixed reflexive,passive,it+ relations, should be unary [24 March 2011 Diana McCarthy]
# - Modified so modifier/modified is more general (not distinguishing noun-modifiers and adj-modifiers for nouns,
#   and covering adverbs too [27 July 2011 Adam Kilgarriff]
# - Both TRINARY dualized per Adam's request
#   TODO: allow DUAL TRINARY in Manatee and use it here then [15 December 2012 Milos Jakubicek]
# - TRINARY dualized using DUAL (requires Manatee 2.74) [18 February 2013 Milos Jakubicek]
# - allow proper nouns in sketches ("NN.?.?" -> "N.*") [22 Feb 2013 Vojtech Kovar]
# - human-readable gramrel names [26 Nov 2015 Jan Michelfeit]
# - macros and joined possessives [29 Feb 2016 Jan Michelfeit]
# - renamed relations for complements
# - fixed/split "modifies" relation for individual PoS [01 Sep 2016 Milos Jakubicek]
# - fixed pro_possesor relation (switched labels) [02 Jan 2017 Vojtech Kovar]
# - added adv-adv modifier and split UNIMAP for modifies [11 Jan 2017 Vojtech Kovar]
# - added WSPOSLIST [20 Jul 2017 MichalC]

divert(-1)
define(`NOUN',`"N.*[^Z]"')
define(`ADJECTIVE',`"JJ.*"')
define(`VERB',`"V.*"')
define(`VERB_BE',`"VB.*"')
define(`VERB_HAVE',`"VH.*"')
define(`ADVERB',`"RB.*"')
define(`NOT_NOUN',`[tag!="N.*"]')
define(`DETERMINER', `[tag="DT"|tag="PPZ"]')
define(`MODIFIER', `[tag="JJ.*"|tag="RB.*"|tag=","]')
define(`WHO_WHICH_THAT', `[tag="WP"|tag="IN/that"]')
divert

*STRUCTLIMIT s
*DEFAULTATTR tag
*WSPOSLIST ",adjective,-j,adverb,-a,noun,-n,verb,-v"

*FIXORDER ;modifiers of "%w";nouns modified by "%w";adjectives modified by "%w";verbs modified by "%w";objects of "%w";verbs with "%w" as object;subjects of "%w";verbs with "%w" as subject;"%w" and/or ...;prepositional phrases;adjective predicates of "%w";subjects of "be "%w"";"%w" is a ...;instances of "%w";particles after "%w";particles after "%w" with object;objects of "%w %(3.lemma)";verbs with particle "%(3.lemma)" and "%w" as object;pronominal objects of "%w";pronominal subjects of "%w";%w's ...;possessors of "%w";pronominal possessors of "%w";wh-words following "%w";infinitive objects of "%w";-ing objects of "%w";in passive;as reflexive;it's "%w" to ...;complements of "%w";verbs complemented by "%w";adjectives after "%w";verbs before "%w"

="%w" and/or ...
*UNIMAP and/or
*SYMMETRIC
	1:NOUN [word=","]{0,1} [word="and"|word="or"|word=","] DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN
	1:VERB [word=","]{0,1} [word="and"|word="or"|word=","] ADVERB{0,2} 2:VERB & 1.tag = 2.tag
	1:ADJECTIVE [word=","]{0,1} [word="and"|word="or"|word=","]{0,1} ADVERB{0,2} 2:ADJECTIVE & 1.tag = 2.tag

*DUAL
=objects of "%w"/verbs with "%w" as object
*UNIMAP object/object_of
	1:VERB ADVERB{0,2} DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN
	2:NOUN ADVERB{0,2} 1:"V.N"
	2:NOUN WHO_WHICH_THAT? ADVERB{0,5} VERB_BE ADVERB{0,2} 1:"V.N"

*DUAL
=subjects of "%w"/verbs with "%w" as subject
*UNIMAP subject/subject_of
	2:NOUN WHO_WHICH_THAT? ADVERB{0,3} VERB_BE? ADVERB{0,2} 1:"V.[^N]?"
	2:NOUN WHO_WHICH_THAT? ADVERB{0,3} VERB_BE? ADVERB{0,2} VERB_HAVE ADVERB{0,2} 1:"V.N"
	1:"V.N" ADVERB{0,2} [word="by"] DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN

*DUAL
=adjective predicates of "%w"/subjects of "be %w"
*UNIMAP adj_subject_of/adj_subject
	1:NOUN WHO_WHICH_THAT? ADVERB{0,3} VERB_BE? ADVERB{0,2} 2:ADJECTIVE NOT_NOUN

*DUAL
="%w" is a .../... is a "%w"
*UNIMAP predicate_of/predicate
	1:NOUN WHO_WHICH_THAT? ADVERB{0,5} VERB_BE ADVERB{0,2} DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN

=pronominal objects of "%w"
*UNIMAP pro_object
	1:VERB ADVERB{0,2} 2:[tag="PP" & word!="I" & word!="he" & word!="she" & word!="we" & word!="they"]

=pronominal subjects of "%w"
*UNIMAP pro_subject
	2:"PP" ADVERB{0,3} VERB_BE? ADVERB{0,2} 1:[tag="V.[^N]?"]
	2:"PP" ADVERB{0,5} VERB_BE ADVERB{0,2} 1:"V.N"

*DUAL
=modifiers of "%w"/nouns modified by "%w"
*UNIMAP modifier/n_modifies
	2:"(JJ.*|N.*[^Z])" MODIFIER{0,3} NOUN{0,2} 1:NOUN NOT_NOUN

*DUAL
=modifiers of "%w"/adjectives modified by "%w"
*UNIMAP modifier/j_modifies
	2:"RB" 1:[tag="JJ.*"]

*DUAL
=modifiers of "%w"/verbs modified by "%w"
*UNIMAP modifier/v_modifies
	2:"RB" 1:[tag="V.*"]
	1:VERB ADVERB{0,2} 2:"RB" [tag!="RB.*" & tag!="JJ.*"]

*DUAL
=modifiers of "%w"/adverbs modified by "%w"
*UNIMAP modifier/r_modifies
	2:ADVERB 1:ADVERB


*DUAL
=%w's .../possessors of "%w"
*UNIMAP possessed/possessor
	1:"N.*Z" "CD"{0,2} MODIFIER{0,3} NOUN{0,1} 2:NOUN NOT_NOUN

=pronominal possessors of "%w"
*UNIMAP pro_possessor
	2:"PPZ" "CD"{0,2} MODIFIER{0,3} NOUN{0,1} 1:NOUN NOT_NOUN

=wh-words following "%w"
*UNIMAP wh_comp
	1:VERB ADVERB{0,2} 2:[tag="W.*"]

=infinitive objects of "%w"
*UNIMAP infin_comp
	1:VERB ADVERB{0,2} "TO" ADVERB{0,2} 2:"V.P?"
	1:ADJECTIVE "RB"{0,1} "TO" ADVERB{0,2} 2:"V.P?"

=-ing objects of "%w"
*UNIMAP ing_comp
	1:VERB ADVERB{0,3} 2:"V.G"

*UNARY
=in passive
*UNIMAP passive
	[tag="N.*"|tag="PU."] ADVERB{0,5} 1:"V.N"

*UNARY
=as reflexive
*UNIMAP reflexive
	1:VERB [tag="PP" & word = ".*sel[fv].*"]

*UNARY
=it's "%w" to ...
*UNIMAP it+
	[word="it"] ADVERB{0,3} VERB_BE? ADVERB{0,2} 1:ADJECTIVE ADVERB{0,2} [tag="IN/that"|tag="PP"|tag="TO"]
	[word="it"] ADVERB{0,3} VERB_BE? ADVERB{0,2} DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 1:NOUN "TO"
	[word="it"] ADVERB{0,3} VERB_BE? ADVERB{0,2} DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 1:NOUN [word="for"] "PP" "TO"

*SEPARATEPAGE prepositional phrases
*DUAL
*TRINARY
="%w" %(3.lemma) .../... %(3.lemma) "%w"
	1:[tag="N.*"|tag="JJ.*"] 3:"IN" DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN
	1:VERB ADVERB{0,2} 3:"IN" DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN

*DUAL
=complements of "%w"/verbs complemented by "%w"
*UNIMAP np_adj_comp/np_adj_comp_of
	1:VERB ADVERB{0,2} DETERMINER{0,1} MODIFIER{0,3} NOUN{0,1} NOUN ADVERB{0,2} 2:ADJECTIVE NOT_NOUN
	1:VERB ADVERB{0,2} "PP" ADVERB{0,2} 2:ADJECTIVE NOT_NOUN

*DUAL
=adjectives after "%w"/verbs before "%w"
*UNIMAP adj_comp/adj_comp_of
	1:VERB ADVERB{0,2} 2:ADJECTIVE [tag!="N.*" & tag!="CC" & tag!="JJ.*"]

=particles after "%w"
*UNIMAP part_intrans
	1:VERB 2:"RP" [!(tag="DT"|tag="PPZ"|tag="CD"|tag="JJ.*"|tag="N.*")]

=particles after "%w" with object
*UNIMAP part_trans
	1:VERB 2:"RP" [tag="DT"|tag="PPZ"|tag="CD"|tag="JJ.*"|tag="N.*"]
	1:VERB "PP" 2:"RP"
	1:VERB DETERMINER{0,1} MODIFIER{0,3} NOUN{0,1} NOUN 2:"RP"

*DUAL
*TRINARY
=objects of "%w %(3.lemma)"/verbs with particle "%(3.lemma)" and "%w" as object
	1:VERB 3:"RP" DETERMINER{0,1} "CD"{0,2} MODIFIER{0,3} NOUN{0,2} 2:NOUN NOT_NOUN
