# Word Sketch
###This package is an open-source alternative to the SketchEngine's "word sketch" functionality.

It can be used to:
* Load language corpora and tag their contents by parts of speech and word roots
* Parse tagged corpora with a sketch grammar, searching for all of the collocations in them and saving them in a file
* Load tagged corpora, and write out the strongest collocations of a specific word (a "word sketch" of that word)
* Load tagged corpora, and write out common collocations of two words. This function is not fully implemented yet, right
now it simply writes out the strongest collocations of word 1 that also occur as collocations of word 2
***
**Relevant information:**
* Strength of a specific collocation is calculated by the logDice formula, developed by SketchEngine for this purpose
* Sketch grammars used by SketchEngine can be downloaded from their site, but they need to be parsed with m4 by hand 
before being used with this package
* Tagged corpora in the KPWr format can be used, but this format needs to be specified in the arguments of the 
"parse_corpus" function
* This package can be used in the Constellate environment; in that situation, the function "tag_constellate_corpus" 
should be used, instead of the regular "tag_corpus"
* The sketch grammar and the tagged corpus must use the same tagging format. The built-in corpus tagger uses the default 
tagging format of the nltk package, but not all sketch grammars use it.
***
#####Created by Agata Jakubiak
#####Licensing information can be found in the file LICENCE.txt
