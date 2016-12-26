import os
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag, ne_chunk, word_tokenize
from nltk.tokenize import SpaceTokenizer
from nltk.tree import Tree


# A container class for storing company information. 
class CompanyInfo():
    def __init__(self, csvRow):
        self.companyName = csvRow[0]
        self.asxCode = csvRow[1]
        self.gicsIndustryGroup = csvRow[2]
        self.aliases = csvRow[3]
        self.ceoAliases = csvRow[4]
        self.companyNameModified = ''
        self.removedWords = ''
        self.businessArea = ''
        self.location = ''

# A container class for storing the output from the headline parser. 
# Each company mentioned in a headline is assigned its own instance of this class. 
class HeadlineResult():
    def __init__(self, timestamp, companyCode, confidenceOfCode, sentiment, keywordList):
        self.timestamp = timestamp
        self.companyCode = companyCode
        self.confidenceOfCode = confidenceOfCode #How reliably we think that this company code cas been mentioned in the article. 
        self.sentiment = sentiment
        self.keywordList = keywordList

# Reads headlines, determines if company is mentioned and gauges sentiment. 
class HeadlineParser():
    # Level 0
    def __init__ (self, companyNamesPath):
        self.companyInfo = self._loadCompanyInfo(companyNamesPath)
        # Create the sentiment analyser. 
        self.sentiment = SentimentIntensityAnalyzer()
        self.tokenizer = SpaceTokenizer()

    # Level 0
    # Return one headline result object for each company we think is mentioned or affected by this article. 
    def parseHeadline(self, headline, dateString):
        resultList = []

        sentiment = self._getSentiment(headline)

        headlineNames = self._getProperNouns(headline)

        codes, confidences = self._matchCompanyToName(headlineNames)

        for index in range(len(codes)):
            resultList.append(HeadlineResult(dateString, codes[index], confidences[index], sentiment, ''))

       # for name in properNouns:
            ## Find likely matches between the named entities from the headline and the list of asx 200 companies.

            #resultList.append(HeadlineResult(dateString, name, sentiment, ''))
        return resultList
    # Level 1
    def _matchCompanyToName(self, names)
        companyCodes = []
        companyConfidences = []
        for name in names:
            
            for index in range(len(self.companyInfo)):
                # if company info has aliases, use those instead of the name
                # if company info has ceo names or notable people, use those as well
                # test the company name by itself first, then try with business area words, then try with company structure words.


                # Add the results of all of these tests together to give a combined confidence. 
    
    # Level 1
    def _loadCompanyInfo(self, filePath):
        companyInfo = []
        #print('Importing company names data...')
        with open(os.path.join(filePath)) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                companyInfo.append(CompanyInfo([column.upper() for column in row]))

        companyStructureWords = ['THE', ' LIMITED', ' LTD', ' COMPANY', ' FUND', ' CORPORATION', ' PLC', ' HOLDINGS', ' GROUP', ' INCORPORATED', ' CONSOLIDATED', ' ENTERPRISES', ' STAPLED', ' NZX', ' NZ', ' CO.', ' FORUS', ' TRUST']

        businessAreaWords = [' MINING', ' PETROLEUM', ' COMMUNICATIONS', ' SERVICES', ' RESOURCES', ' MINERALS', ' ENTERTAINMENT', ' PROPERTY', ' MINERAL', ' HEALTHCARE', ' HEALTH CARE', ' INVESTMENTS', ' AIRWAYS', ' AIR WAYS', ' LEISURE', ' ENERGY', ' TRAVEL', ' METALS', ' COAL', ' BANKING', ' MEDIA', ' BUILDING', ' TELECOM', ' HEALTH', ' INVESTMENT', ' MANAGEMENT', ' METAL', ' PHARMACEUTICALS', ' ASSET', ' FINANCIAL', ' ROADS', ' INDUSTRIES', ' PROPERTIES',  ' LIFESTYLE', ' RESORTS', ' STEEL', ' WASTE', ' RETAIL', ' MEDICAL', ' TELEVISION', ' MORTGAGE', ' INSURANCE', ' ADMINISTRATION', ' CARE', ' PHARMACEUTICAL', ' AGRICULTURAL', ' ORD UNITS']
        locationWords = [' AUSTRALASIA', ' AUSTRALIA', ' WORLDWIDE', ' GLOBAL', ' PACIFIC', ' NEW ZEALAND']

        for index in range(len(companyInfo)):

            nameModified, removedWords = self._removeSelectedWords(companyInfo[index].companyName, companyStructureWords)
            companyInfo[index].companyNameModified = nameModified
            companyInfo[index].removedWords = removedWords
 
            nameModified, businessArea = self._removeSelectedWords(companyInfo[index].companyNameModified, businessAreaWords)
            companyInfo[index].companyNameModified = nameModified
            companyInfo[index].businessArea = businessArea

            nameModified, location = self._removeSelectedWords(companyInfo[index].companyNameModified, locationWords)
            companyInfo[index].companyNameModified = nameModified
            companyInfo[index].location = location
            
        return companyInfo

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
        return 0    

    # Level 2
    def _removeSelectedWords(self, name, wordsToRemove):
        removedWords = ''
        for word in wordsToRemove:
            if word in name:
                removedWords += word
            name = name.replace(word, '')

        name = name.replace('    ', ' ')
        name = name.replace('   ', ' ')
        name = name.replace('  ', ' ')

        name = name.strip()
        removedWords = removedWords.strip()
        return name, removedWords

if __name__ == "__main__":
    headlineparser = HeadlineParser('20161201-asx200.csv')
    for company in headlineparser.companyInfo:
        print company.companyNameModified + '   ' + company.businessArea + '   ' + company.location + '   ' + company.removedWords
    dateString = '01_Jan_2016'

    headlineList = ["China weakens its stance on abortion. I feel good about it.", "Explosion in Altura factory linked to operational defects.", "Sabotage on SpaceX rocket not yet ruled out.", "4 dead on Dreamworld ride.", "Bega's Barry Irvin can't find the magic formula to crack Chinese market", "Nescafe sued Moccona for $100m.", "Ardent CEO to address Dreamworld tragedy"]
   # for line in headlineList:
   # 
   #     resultList = headlineparser.parseHeadline(line, dateString)
   #     for result in resultList:
   #         print result.companyCode
   #         print result.sentiment

   # dateString = ""
   # # Test the ability of the NER to find company name from other usesless words like limited or company. 
   # for company in headlineparser.companyInfo:
   # 
   #     resultList = headlineparser.parseHeadline(company.companyName, dateString)
   #     for result in resultList:
   #         print company.companyName, "  ", result.companyCode, "  ", str(result.sentiment) 
            
