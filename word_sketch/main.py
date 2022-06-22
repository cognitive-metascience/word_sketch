import grammar_structure
import grammar_import

print()
print("Gramatyka j. francuskiego:")


#ta funkcja wczytuje plik z korpusem, przetwarza go, i zapisuje w obiekcie 'Corpus' jako listę obiektów "Word", które zawierają
#informacje o treści, tagu, i lemmie każdego słowa po kolei.
corpus=grammar_structure.Corpus("files/korpus_trojjezyczny__french.vert")

#ta funkcja wczytuje plik z gramatyką powierzchniową, przetwarza ją, i zapisuje w obiekcie "Grammar" jako listę obiektów "Collocation",
#które zawierają informacje o nazwie każdej wyszukiwanej kolokacji, i wyszukiwaniach które służą do znalezienia jej
grammar=grammar_import.read_grammar_file("files/fr_gram.txt")

#w tej funkcji gramatyka przyjmuje korpus i lemmę, i wyszukuje w korpusie wszystkie występowania tej lemmy które pasują do kolokacji
#zapisanych w gramatyce
#grammar.find("global",corpus)

#zamiast wypisywania, szkic słowa powstaje jako słownikopodobny obiekt i jest zapisany na zmienną
sketch1 = grammar_import.WordSketch(grammar.find2("global",corpus))
sketch1.writeout() #można go też wypisać - wygląda to jak poprzednio (czyli przy funkcji find)

print()
print("Gramatyka j. polskiego:")
grammar=grammar_import.read_grammar_file("files/pl_gram.txt")
corpus=grammar_structure.Corpus("files/aktualnosci_uw_litopad_2021.vert")
sketch2 = grammar_import.WordSketch(grammar.find2("uniwersytet",corpus))
sketch2.writeout()
sketch3 = grammar_import.WordSketch(grammar.find2("student",corpus))
#sketch3.writeout()

print()
print("Gramatyka j. angielskiego:")
corpus=grammar_structure.Corpus("files/en_pln__english.vert")
grammar=grammar_import.read_grammar_file("files/en_gram.txt")
sketch4 = grammar_import.WordSketch(grammar.find2("union",corpus))
sketch4.writeout()

#tutaj przykładowa operacja porównania na dwóch szkicach słów
print()
print("Porównanie szkiców słów dla 'uniwersytet' i 'student': \n")
sketch2.word_difference(sketch3)

#KPWr
print("Korzystanie z KPWr")
corpus=grammar_structure.Corpus("files/KPWr/00100622.xml", KPWr=True)
#corpus.writeout()