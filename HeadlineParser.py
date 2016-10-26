import os
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag, ne_chunk, word_tokenize
from nltk.tokenize import SpaceTokenizer
from nltk.tree import Tree

# A container class for storing company names information. 
class CompanyNames():
    def __init__(self, csvRow):
        self.companyName = csvRow[0]
        self.asxCode = csvRow[1]
        self.gicsIndustryGroup = csvRow[2]


# A container class for storing the output from the headline parser. 
# Each company mentioned in a headline is assigned its own instance of this class. 
class HeadlineResult():
    def __init__(self, timestamp, companyCode, sentiment, keywordList):
        self.timestamp = timestamp
        self.companyCode = companyCode
        self.sentiment = sentiment
        self.keywordList = keywordList

# Reads headlines, determines if company is mentioned and gauges sentiment. 
class HeadlineParser():

    def __init__ (self, companyNamesPath):
        self.companyInfo = []
        # Create the sentiment analyser. 
        self.sentiment = SentimentIntensityAnalyzer()
        self.tokenizer = SpaceTokenizer()

        #print('Importing company names data...')
        with open(os.path.join(companyNamesPath)) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.companyInfo.append(CompanyNames(row))
 

    def parseHeadline(self, headline, dateString):

        properNouns = self._getProperNouns(headline)

        #companyNames = self._getValidCompanyName(headline)
        #print companyNames

        sentiment = self._getSentiment(headline)
        resultList = []

        for name in properNouns:
            resultList.append(HeadlineResult(dateString, name, sentiment, ''))

        return resultList

    
    def _getValidCompanyName(self, headline):

        wordList = self.tokenizer.tokenize(headline)

        validNames = []        
        print wordList
        for word in wordList:
            modifiedWord = word.lower().replace(' ', '')
            print modifiedWord
            for company in self.companyInfo:
                modifiedName = company.companyName.lower().replace(' ', '')
                if modifiedWord in modifiedName:
                    validNames.append(company.asxCode)
                    print modifiedName

        
        return validNames

    ## Identify named entities within a string of text. 
    # Return a list containing a string for each entity name. 
    def _getProperNouns(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        prev = None
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue

        return continuous_chunk

    ## Identify the sentiment of a string of text. 
    # Return a float between -1 and 1. 
    def _getSentiment(self, headlineString):

        # Empty list to be filled with sentiment values. 
        sentimentList = []
        sentenceList = tokenize.sent_tokenize(headlineString)

        for sentence in sentenceList:
            ss = self.sentiment.polarity_scores(sentence)
            sentimentList.append(ss['compound'])

        # Resulting sentiment is the average of each of the sentences in headline.
        return sum(sentimentList) / float(len(sentimentList)) 

    def _getKeyWords(self, headlineString):
        


if __name__ == "__main__":
    
    headlineparser = HeadlineParser('ASXListedCompanies.csv')

    dateString = '01_Jan_2016'

    headlineList = ["China weakens its stance on abortion. I feel good about it.", "Explosion in Altura factory linked to operational defects.", "Sabotage on SpaceX rocket not yet ruled out.", "4 dead on Dreamworld ride.", "Bega's Barry Irvin can't find the magic formula to crack Chinese market", "Nescafe sued Moccona for $100m.", "Ardent CEO to address Dreamworld tragedy"]
    for line in headlineList:
    
        resultList = headlineparser.parseHeadline(line, dateString)
        for result in resultList:
            print result.companyCode
            print result.sentiment
