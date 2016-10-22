from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag, ne_chunk
from nltk.tokenize import SpaceTokenizer

tokenizer = SpaceTokenizer()

#headline = "I never said that it wasn't good. Yet, I could not want something more. Danger on the horizon. Explosion linked to operational defects. China weakens it's stance on abortion. US not willing to falter on climate change."

headline = "China weakens it's stance on abortion."


toks = tokenizer.tokenize(headline)
print toks
pos = pos_tag(toks)
chunked_nes = ne_chunk(pos) 

nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]

print nes

sentences = tokenize.sent_tokenize(headline)
print sentences
"""
sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    print ss
    print ''


"""
