import cqls
import nltk
import regex
import grammar_structure
import grammar_import
print()
print("Word sketch słowa \"global\" w korpusie j. francuskiego:")
corpus=grammar_structure.Corpus("files/korpus_trojjezyczny__french.vert")
grammar=grammar_import.read_grammar_file("files/fr_gram.txt")
grammar.find("global",corpus)

print()
print("Word sketch słowa \"uniwersytet\" w korpusie j. polskiego:")
corpus=grammar_structure.Corpus("files/aktualnosci_uw_litopad_2021.vert")
grammar=grammar_import.read_grammar_file("files/pl_gram.txt")
grammar.find("uniwersytet",corpus)

print()
print("Word sketch słowa \"union\" w korpusie j. angielskiego:")
corpus=grammar_structure.Corpus("files/en_pln__english.vert")
grammar=grammar_import.read_grammar_file("files/en_gram.txt")
grammar.find("union",corpus)
