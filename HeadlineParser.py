import os
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag, ne_chunk
from nltk.tokenize import SpaceTokenizer

# A container class for storing company names information. 
class CompanyNames():
    def __init__(self, csvRow):
        self.companyName = csvRow[0]
        self.asxCode = csvRow[1]
        self.gicsIndustryGroup = csvRow[2]

class HeadlineParser():

    def __init__ (self, companyNamesPath):
        self.companyNames = []

        print('Importing company names data...')
        with open(os.path.join(companyNamesPath)) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.companyNames.append(CompanyNames(row))
 

    def parseHeadline(self, headline, dateString):

        properNouns = self._getProperNouns(headlineString)

        properNouns = self._getProperNouns(headlineString)
        companyNames = self._getValidCompanyname(properNounList)

        # Ignore headlines if more than one company is discussed. 
        if len(companynames) >1:
            quit()
        else:
            companyName = companyNames[0]

        sentiment = self._getSentiment(headlineString)

        dateTime = dateString 

    def _getSentiment(self, headlineString):
        # Create the sentiment analyser. 
        sid = SentimentIntensityAnalyzer()

        # Empty list to be filled with sentiment values. 
        sentimentList = []
        sentenceList = tokenize.sent_tokenize(headlineString)

        for sentence in sentenceList:
            ss = sid.polarity_scores(sentence)
            print ss['compound']
            sentimentList.append(ss['compound'])

        # Resulting sentiment is the average of each of the sentences in headline.
        return sum(sentimentList) / float(len(sentimentList)) 

    def _getProperNouns(self, headlineString):

        tokenizer = SpaceTokenizer()
        toks = tokenizer.tokenize(headline)
        print toks
        pos = pos_tag(toks)
        print pos
        chunked_nes = ne_chunk(pos) 
        print chunked_nes

        nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
        print nes

    def _getValidCompanyName(self, properNounsList):

        return 1


if __name__ == "__main__":
    
    headline = "China weakens its stance on abortion. I feel good about it."
    #headline = "I never said that it wasn't good. Yet, I could not want something more. Danger on the horizon. Explosion linked to operational defects. China weakens it's stance on abortion. US not willing to falter on climate change."

    #headline = "Sabotage on SpaceX rocket explosion turns out to be possible"
    #headline = "Altura mining stocks set to plummet"

    #headline = "SpaceX's 'Raptor Rocket' to send humans to Mars"

    headlineparser = HeadlineParser('ASXListedCompanies.csv')

    sentiment = headlineparser._getSentiment(headline)
    print sentiment
    


