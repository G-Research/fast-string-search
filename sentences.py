from nltk.corpus import webtext, brown, gutenberg, reuters


def get_sentences(corpus):
    for fileid in corpus.fileids():
        for sentence in corpus.sents(fileid):
            yield " ".join(sentence)

SENTENCES = []
for corpus in (webtext, brown, gutenberg, reuters):
    SENTENCES.extend(get_sentences(corpus))
print(f"LOADED {len(SENTENCES)} SENTENCES")
