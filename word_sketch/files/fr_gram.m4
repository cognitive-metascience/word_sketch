# Sketch Grammar for French, FreeLing/EAGLES tagset
# ver. 1.6
#
# Changelog
# - Initial version. [8 March 2006, Adam Kilgarriff]
# - added *UNIMAP directives [9 Oct 2013, Vojta Kovar]
# - some UNIMAP corrected [7 Jul 2014, Vit Baisa]
# - proper nouns added as per customer request [13 Aug 2014, Milos Jakubicek]
# - relations for prepositions (customer request) [30 Aug 2015, Vojta Kovar]
# - fixed modifier relation [30 Aug 2015, Vojta Kovar]
# - added WSPOSLIST [20 Jul 2017 MichalC]
# - improved by Ludovica Lanini [23 Nov 2017; intership in LCC, <ludovica.lanini@uniroma1.it>]
# - fixed wrong format of tags & CQL; added relations for prepositions
# - rewrote with macros and changed tagset to EAGLES [20 Jun 2019, Jan Michelfeit]

*STRUCTLIMIT s
*DEFAULTATTR tag
*WSPOSLIST ",noun,-n,verb,-v,adjective,-j,adverb,-r"
*FIXORDER ;objects of "%w";verbs with "%w" as object;subjects of "%w";verbs with "%w" as subject;modifiers of "%w";nouns modified by "%w";adjectives modified by "%w";verbs modified by "%w";"%w"and/or...;prepositional phrases with nouns;prepositional phrases with verbs;adjective predicates of "%w";subjects of "être %w";"%w" is a ...;pronominal objects of "%w";pronominal subjects of "%w";pronominal possessors of "%w";infinitive objects of "%w";adjectives after "%w";verbs before "%w";prepositions preceeding noun;nouns after preposition

divert(-1)
define(`NOUN',`"N.*"')
define(`COMMON_NOUN',`"NC.*"')
define(`ADJECTIVE',`"A.*"')
define(`ADVERB',`"R.*"')
define(`VERB',`"V.*"')
define(`VERB_BE',`"VS.*"')
define(`VERB_HAVE',`"VA.*"')
define(`VERB_INFI',`"V.N.*"')
define(`VERB_NORMAL',`"VM[^NP].*"') # lexical verb, neither infinitive or participle
define(`VERB_PASTPART',`[tag="V.P.*" & lc!=".*nt"]')
define(`VERB_NOT_BE_PASTPART',`[tag="V[^S]P.*" & lc!=".*nt"]')
define(`COMMA',`[word=","]')
define(`DETERMINER', `"D.*"')
define(`POSSESSIVE_DETERMINER', `"DP.*"')
define(`PREPOSITION', `"SP.*"')
define(`PRONOUN', `"P.*"')
define(`INDEFINITE_PRONOUN', `"PI.*"')
define(`PERSONAL_PRONOUN', `"PP.*"')
define(`DEMONSTRATIVE_PRONOUN', `"PD.*"')
define(`CONJUNCTION', `"C.*"')
define(`NUMERAL', `"Z.*"')
define(`NOT_NOUN_ADJ_ADV', `"[^ANR]"')
divert

="%w" and/or ...
*UNIMAP and/or
*SYMMETRIC
1:NOUN ADJECTIVE{0,3} COMMA? [lemma="et" | lemma="ou" | word=","] [lemma="de"]? (DETERMINER|PREPOSITION)? NUMERAL{0,2} (ADJECTIVE|ADVERB|COMMA){0,3} 2:NOUN
1:VERB COMMA? [lemma="et" | lemma="ou" | word=","] [lemma="de"]? (VERB_BE|VERB_HAVE|ADVERB|COMMA){0,3} 2:VERB
1:ADJECTIVE (ADJECTIVE|ADVERB|COMMA){0,3} [lemma="et" | lemma="ou" | word=","] (ADJECTIVE|ADVERB|COMMA){0,3} 2:ADJECTIVE
1:ADJECTIVE COMMON_NOUN 2:ADJECTIVE
# ni_ni | neither_nor
[word="ni"] (DETERMINER|NUMERAL)? ADJECTIVE? 1:COMMON_NOUN ADJECTIVE{0,3} (PREPOSITION COMMON_NOUN ADJECTIVE?)? [lemma="ni"] (DETERMINER|NUMERAL)? ADJECTIVE? 2:COMMON_NOUN
[word="ni"] (DETERMINER|NUMERAL)? ADJECTIVE? COMMON_NOUN? 1:ADJECTIVE (PREPOSITION COMMON_NOUN ADJECTIVE?)? [lemma="ni"] (DETERMINER|NUMERAL)? 2:ADJECTIVE
[word="ni|ne|n'"] ADVERB{0,2} 1:VERB DETERMINER? ADJECTIVE? COMMON_NOUN? ADJECTIVE? ADVERB{0,2} [lemma="ni"] ADVERB{0,2} 2:VERB & 1.tag=2.tag
# "%w" mais | "%w" but
COMMON_NOUN? 1:ADJECTIVE COMMON_NOUN? [lemma="mais"] COMMON_NOUN? 2:[tag=ADJECTIVE & word!="bon"]


*DUAL
=objects of "%w"/verbs with "%w" as object
*UNIMAP object/object_of
1:[tag=VERB & lemma!=".{1,2}" & tag!=VERB_BE] ADVERB{0,2} DETERMINER? (NUMERAL|ADJECTIVE|ADVERB){0,2} 2:[tag=NOUN & lemma!=".{1,2}"]
2:[tag=NOUN & lemma!=".{1,2}"] (ADJECTIVE|ADVERB){0,2} 1:VERB_PASTPART


* DUAL
=subjects of "%w"/verbs with "%w" as subject
*UNIMAP subject/subject_of
([tag!=PREPOSITION]{3} | <s> [tag!=PREPOSITION]{0,2}) 2:[tag=NOUN & lemma!=".{1,2}"] (ADVERB|PRONOUN){0,2} VERB_HAVE (ADVERB|PRONOUN){0,2} 1:VERB_NOT_BE_PASTPART
([tag!=PREPOSITION]{3} | <s> [tag!=PREPOSITION]{0,2}) 2:[tag=NOUN & lemma!=".{1,2}"] (ADVERB|PRONOUN){0,2} 1:VERB_NORMAL


*DUAL
=adjective predicates of "%w"/subjects of "être %w"
*UNIMAP adj_subject/adj_subject_of
1:[tag=NOUN & lemma!=".{1,2}"] ADVERB{0,2} VERB_BE ADVERB{0,2} 2:ADJECTIVE NOT_NOUN_ADJ_ADV


*DUAL
="%w" is a .../... is a "%w"
*UNIMAP predicate/predicate_of
1:[tag=NOUN & lemma!=".{1,2}"] ADVERB{0,2} VERB_BE (ADJECTIVE|ADVERB|DETERMINER){0,3} 2:NOUN NOT_NOUN_ADJ_ADV


*DUAL
=modifiers of "%w"/nouns modified by "%w"
*UNIMAP modifier/modifies
2:[tag=ADJECTIVE & lemma!=".{1,2}"] 1:COMMON_NOUN
1:COMMON_NOUN (ADJECTIVE|CONJUNCTION)? 2:[tag=ADJECTIVE & lemma!=".{1,2}"]


*DUAL
=modifiers of "%w"/verbs modified by "%w"
*UNIMAP modifier/modifies
1:VERB (DETERMINER|NUMERAL)? ADJECTIVE? COMMON_NOUN? 2:[tag=ADVERB & lemma!="pas"]
(VERB_BE|VERB_HAVE) 2:[tag=ADVERB & lemma!="pas"] 1:VERB_PASTPART


*DUAL
=modifiers of "%w"/adjectives modified by "%w"
*UNIMAP modifier/modifies
2:[tag=ADVERB & lemma!="plus|pas|très|non"] 1:ADJECTIVE


*DUAL
=noun modifiers of "%w"/nouns modified by noun "%w"
*UNIMAP modifier/modifies
(DETERMINER|ADJECTIVE|PRONOUN) 1:COMMON_NOUN 2:COMMON_NOUN


=infinitive objects of "%w"
*UNIMAP infin_comp
1:VERB (ADVERB|PERSONAL_PRONOUN){0,3} 2:VERB_INFI


*DUAL
=adjectives after "%w"/verbs before "%w"
*UNIMAP adj_comp/adj_comp_of
1:[tag=VERB & lemma="apparaître|demeurer|devenir|paraître|rester|sembler|estimer|trouver|appeler|juger|rendre|nommer|proclamer|considérer|déclarer| désigner|créer|réputer|vivre|naître|mourir|tomber|élir|reconnaître|croire|faire|voir|partir|sortir|monter|venir|rentrer"] ADVERB{0,3} 2:ADJECTIVE


*DUAL
=more/less "%w" than ...
[lemma="plus|moins|aussi"] 1:ADJECTIVE [lemma="que"] 2:ADJECTIVE
[lemma="plus|moins|aussi"] 1:ADJECTIVE [lemma="que"] (DETERMINER|DEMONSTRATIVE_PRONOUN|NUMERAL)? 2:COMMON_NOUN


*SEPARATEPAGE prepositional phrases
*TRINARY
="%w" %(3.lemma)
1:"[NAV].*" 3:PREPOSITION (DETERMINER|NUMERAL|ADJECTIVE){0,3} 2:NOUN
1:"[NAV].*" 3:PREPOSITION (DETERMINER|NUMERAL|ADJECTIVE){0,3} 2:VERB_INFI


=pronominal objects of "%w"
*UNIMAP pro_object
2:[tag=PERSONAL_PRONOUN & word="me|m'|te|t'|le|la|les|se"] 1:VERB_NORMAL
2:[tag=PERSONAL_PRONOUN & word="nous"] 1:[tag=VERB_NORMAL & word!=".*ns" & word!=".*mes" ]
2:[tag=PERSONAL_PRONOUN & word="vous"] 1:[tag=VERB_NORMAL & word!=".*ez" & word!=".*tes" ]
2:[tag=PERSONAL_PRONOUN & word="me|m'|te|t'|le|la|les|se"] VERB_BE ADVERB{0,2} 1:VERB_NOT_BE_PASTPART
2:[tag=PERSONAL_PRONOUN & word="nous"] [tag=VERB_BE & word!=".*ns"] ADVERB{0,2} 1:VERB_NOT_BE_PASTPART
2:[tag=PERSONAL_PRONOUN & word="vous"] [tag=VERB_BE & word!=".*ez"] ADVERB{0,2} 1:VERB_NOT_BE_PASTPART


=pronoun is "%w"
2:[tag=PERSONAL_PRONOUN & word="je|tu|il|elle|ils|elles|on"] ADVERB{0,3} VERB_BE ADVERB{0,3} 1:ADJECTIVE
2:[tag=PERSONAL_PRONOUN & word="je|tu|il|elle|ils|elles|on"] VERB_BE ADVERB{0,3} [lc="été"] ADVERB{0,3} 1:ADJECTIVE
2:[tag=PERSONAL_PRONOUN & word="nous"] ADVERB{0,3} [tag=VERB_BE & word=".*ns|.*mes"] ADVERB{0,3} 1:ADJECTIVE
2:[tag=PERSONAL_PRONOUN & word="vous"] ADVERB{0,3} [tag=VERB_BE & word=".*ez|.*tes"] ADVERB{0,3} 1:ADJECTIVE
2:[tag=PERSONAL_PRONOUN & word="nous"] [tag=VERB_BE & word=".*ns|.*mes"] ADVERB{0,3} [lc="été"] ADVERB{0,3} 1:ADJECTIVE
2:[tag=PERSONAL_PRONOUN & word="vous"] [tag=VERB_BE & word=".*ez|.*tes"] ADVERB{0,3} [lc="été"] ADVERB{0,3} 1:ADJECTIVE


=pronominal possessors of "%w"
*UNIMAP pro_possessor
2:POSSESSIVE_DETERMINER ADJECTIVE{0,3} 1:COMMON_NOUN


=pronominal subjects of "%w"
*UNIMAP pro_subject
2:[tag=PERSONAL_PRONOUN & word="je|tu|il|elle|ils|elles|on"] ADVERB* PERSONAL_PRONOUN* 1:VERB_NORMAL
2:[tag=PERSONAL_PRONOUN & word="nous"] ADVERB* PERSONAL_PRONOUN? 1:[tag=VERB_NORMAL & word=".*ns|.*mes"]
2:[tag=PERSONAL_PRONOUN & word="vous"] ADVERB* PERSONAL_PRONOUN? 1:[tag=VERB_NORMAL & word=".*ez|.*tes"]
2:[tag=PERSONAL_PRONOUN & word="je|tu|il|elle|ils|elles|on"] ADVERB* PERSONAL_PRONOUN* VERB_BE ADVERB{0,2} 1:VERB_PASTPART
2:[tag=PERSONAL_PRONOUN & word="nous"] ADVERB* PERSONAL_PRONOUN? [tag=VERB_BE & word=".*ns"] ADVERB{0,2} 1:VERB_PASTPART
2:[tag=PERSONAL_PRONOUN & word="vous"] ADVERB* PERSONAL_PRONOUN? [tag=VERB_BE & word=".*ez"] ADVERB{0,2} 1:VERB_PASTPART
[word="c'"] [word="est"] DETERMINER? 2:PERSONAL_PRONOUN [lemma="qui"] 1:[tag=VERB & tag!=VERB_HAVE & tag!=VERB_BE]
[word="c'"] [word="est"] DETERMINER? 2:PERSONAL_PRONOUN [lemma="qui"] VERB_BE ADVERB{0,2} 1:VERB_PASTPART
#=indefinite pronouns subjects of "%w"
([tag!=PREPOSITION]{3} | <s> [tag!=PREPOSITION]{0,2}) 2:INDEFINITE_PRONOUN (PREPOSITION|COMMON_NOUN)? [tag=PERSONAL_PRONOUN & word!="je|tu|il|elle|ils|elles|on"]? 1:VERB_NORMAL
([tag!=PREPOSITION]{3} | <s> [tag!=PREPOSITION]{0,2}) 2:INDEFINITE_PRONOUN (PREPOSITION|COMMON_NOUN)? [tag=PERSONAL_PRONOUN & word!="je|tu|il|elle|ils|elles|on"]? 1:VERB_BE ADVERB{0,2} VERB_PASTPART


=prepositions preceeding noun/nouns after preposition
2:PREPOSITION (DETERMINER|NUMERAL|ADJECTIVE){0,4} 1:NOUN


*UNARY
=aller "%w"
[lemma="aller"] 1:VERB_INFI

*UNARY
=venir de "%w"
[lemma="venir"] [word="de"] 1:VERB_INFI

*UNARY
=devoir "%w"
[lemma="devoir"] 1:VERB_INFI

*UNARY
=pouvoir "%w"
[lemma="pouvoir"] 1:VERB_INFI

*UNARY
=être en train de "%w"
VERB_BE [lemma="en"] [lemma="train"] [lemma="de"] 1:VERB_INFI

*UNARY
=with_indefinite_article
    [lemma="un"] (NUMERAL|ADJECTIVE|ADVERB){0,2} 1:NOUN

*UNARY
=with_definite_article
    [lemma="le"] (NUMERAL|ADJECTIVE|ADVERB){0,2} 1:NOUN

