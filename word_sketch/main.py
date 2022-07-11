import word_sketch

#word_sketch.tag_corpus("files/tmp/paths.txt","files/corpora/OANC_written_en.txt","en")

word_sketch.parse_corpus("files/corpora/aktualnosci_uw_pl.vert", "files/grammars/IPI_PAN_1.1_pl.txt","files/parsed_corpora/aktualnosci_uw_IPI_PAN_1.1_pl.p")
word_sketch.parse_corpus("files/corpora/OANC_spoken_en.txt", "files/grammars/penn_3.1_en.txt","files/parsed_corpora/OANC_spoken_penn_3.1_en.p")


word_sketch.common_collocations_in_parsed_corpus("files/parsed_corpora/aktualnosci_uw_IPI_PAN_1.1_pl.p","uniwersytet","uczelnia",4)
word_sketch.common_collocations_in_parsed_corpus("files/parsed_corpora/OANC_spoken_penn_3.1_en.p","be","have",amount=4)

word_sketch.search_in_parsed_corpus("files/parsed_corpora/aktualnosci_uw_IPI_PAN_1.1_pl.p", "uniwersytet", 12)
word_sketch.search_in_parsed_corpus("files/parsed_corpora/OANC_spoken_penn_3.1_en.p", "be", amount=12)

word_sketch.parse_corpus("files/KPWr/00100622.xml", "files/grammars/IPI_PAN_1.1_pl.txt","files/parsed_corpora/KPWR_test.p",KPWr=True)
word_sketch.search_in_parsed_corpus("files/parsed_corpora/KPWR_test.p", "problem", amount=12)

