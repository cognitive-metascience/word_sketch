# Word Sketch
### This package is an open-source alternative to the SketchEngine's "word sketch" functionality.

It can be used to:
* Load language corpora and tag their contents by parts of speech and lemmas (word roots)
* Parse tagged corpora with a sketch grammar, searching for all of the collocations in them and saving them in a file
* Load tagged corpora, and write out the strongest collocations of a specific word (a "word sketch" of that word)
* Load tagged corpora, and write out common collocations of two words. This function is not fully implemented yet, right
now it simply writes out the strongest collocations of word 1 that also occur as collocations of word 2
***
**Relevant information:**
* Strength of a specific collocation is calculated by the logDice formula, developed by [Sketch Engine](https://www.sketchengine.eu)  for this purpose
* Sketch grammars used by SketchEngine can be downloaded from their site, but they must be parsed with m4 manually 
before being used with this package
* Tagged corpora in the [KPWr](https://clarin-pl.eu/index.php/kpwr/) format can be used, but this format needs to be specified in the arguments of the 
"parse_corpus" function
* This package can be used in the Constellate environment; in that situation, the function "tag_constellate_corpus" 
should be used, instead of the regular "tag_corpus"
* The sketch grammar and the tagged corpus must use the same tagging format. The built-in corpus tagger uses the default 
tagging format of the nltk package, but not all sketch grammars use it.
***
##### Created by Agata Jakubiak
##### Licensing information can be found in the file LICENCE.txt




## Word Sketch Library Documentation

### Introduction
"Word Sketch" is an open-source alternative to a feature available in SketchEngine, used for analyzing texts and identifying collocations. This documentation explains how to use the code to analyze a single text file or a collection of files.

### Requirements
- Python 3.7+
- Necessary Python packages:
  - `lxml`
  - `nltk`
  - `tqdm`
  - `beautifulsoup4`
  - `cqls`
  
These can be installed using:
```bash
pip install lxml nltk tqdm beautifulsoup4 cqls
```

### File Structure
1. **main.py**: Main scripts to run the analysis.
2. **word_sketch.py**: Core functions such as corpus parsing and collocation detection.
3. **read_KPWr.py**: Functions for reading XML files from the KPWr corpus.
4. **corpus_structure.py**: Classes and functions for representing the corpus.
5. **grammar_structure.py**: Classes and functions for representing the grammar.
6. **query_structure.py**: Classes and functions for representing queries.
7. **grammar_edit.py**: Tools for editing and processing grammars.
8. **README.md**: Project documentation (this file).

### Usage Instructions

#### 1. Preparing the Corpus

The corpus can be in text or XML format. If the file is in XML format (e.g., from the KPWr corpus), use the `read_xml` function from `read_KPWr.py` to convert it to text format.

```python
from read_KPWr import read_xml

# Example of converting an XML file to text format
text = read_xml("path/to/file.xml", save=True, path_to="path/to/save")
```

#### 2. Tagging the Corpus

To prepare the corpus for analysis, it must be pre-tagged. Use the `tag_corpus` or `tag_constellate_corpus` function (if using data from Constellate).

```python
from word_sketch import tag_corpus

# Example of tagging the corpus
tag_corpus("path/to/list_of_files.txt", "path/to/save_tagged_corpus.txt", "en")
```

#### 3. Parsing the Corpus

The `parse_corpus` function processes the corpus, searching for collocations according to a given grammar.

```python
from word_sketch import parse_corpus

# Example of parsing the corpus
parse_corpus("path/to/corpus.txt", "path/to/grammar.txt", "path/to/save/parsed_corpus.p", KPWr=False)
```

The `KPWr` parameter sets whether the corpus is in XML format (default is `False`).

#### 4. Finding Collocations

To find collocations, use the `search_in_parsed_corpus` or `common_collocations_in_parsed_corpus` functions.

```python
from word_sketch import search_in_parsed_corpus, common_collocations_in_parsed_corpus

# Finding collocations for a single lemma
# writes out 'amount' of most common collocates of 'lemma'
search_in_parsed_corpus("path/to/saved_parsed_corpus.p", "lemma", amount)

# Finding common collocations for two lemmas
common_collocations_in_parsed_corpus("path/to/saved_parsed_corpus.p", "lemma1", "lemma2", amount)
```

### Example Usage

The code in `main.py` includes example usage of the above functions. You can adapt it to your needs by providing the appropriate paths for corpus files, grammars, and output locations.

```python
from src.word_sketch import parse_corpus, search_in_parsed_corpus, common_collocations_in_parsed_corpus

def test():
    parse_corpus("path/to/corpus.txt", "path/to/grammar.txt", "path/to/save/parsed_corpus.p")
    search_in_parsed_corpus("path/to/saved_parsed_corpus.p", "lemma", 10)
    common_collocations_in_parsed_corpus("path/to/saved_parsed_corpus.p", "lemma1", "lemma2", 10)

test()
```

### Summary

The "Word Sketch" library enables collocation analysis in textual corpora, providing tools for tagging, parsing, and searching for collocations. It requires proper preparation of input data and grammar configuration. This documentation outlines the basic steps needed to utilize the library's functionality.
