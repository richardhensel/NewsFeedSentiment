import os
import csv
import string


from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk import pos_tag, ne_chunk, word_tokenize
from nltk.tokenize import SpaceTokenizer
from nltk.tree import Tree
from nltk.metrics import *

# A container class for storing company information. 
class CompanyInfo():
    def __init__(self, csvRow):
        self.companyName = csvRow[0]
        self.asxCode = csvRow[1]
        self.gicsIndustryGroup = csvRow[2]
        self.aliases = csvRow[3]
        self.people = csvRow[4]
        self.companyNameModified = ''
        self.removedWords = ''
        self.businessArea = ''
        self.location = ''

# A container class for storing the output from the headline parser. 
# Each company mentioned in a headline is assigned its own instance of this class. 
class HeadlineResult():
    def __init__(self, timestamp, companyCode, confidenceOfCode, sentiment, companyName, keywordList):
        self.timestamp = timestamp
        self.companyCode = companyCode
        self.confidenceOfCode = confidenceOfCode #How reliably we think that this company code cas been mentioned in the article. 
        self.sentiment = sentiment
        self.companyName = companyName
        self.keywordList = keywordList

# Reads headlines, determines if company is mentioned and gauges sentiment. 
class HeadlineParser():
# Level 0
    def __init__ (self, companyNamesPath):
        self.companyInfo = self._loadCompanyInfo(companyNamesPath)
        # Create the sentiment analyser. 
        self.sentiment = SentimentIntensityAnalyzer()
        self.tokenizer = SpaceTokenizer()

    # Return one headline result object for each company we think is mentioned or affected by this article. 
    def parseHeadline(self, headline, dateString):
        resultList = []

        sentiment = self._getSentiment(headline)

        headlineNames = self._getProperNouns(headline)

        codes, confidences, names = self._matchCompanyToName(headlineNames)

        for index in range(len(codes)):
            resultList.append(HeadlineResult(dateString, codes[index], confidences[index], sentiment, names[index], ''))
        return resultList

# Level 1
    def _loadCompanyInfo(self, filePath):
        companyInfo = []
        #print('Importing company names data...')
        with open(os.path.join(filePath)) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                companyInfo.append(CompanyInfo([column.upper() for column in row]))

        companyStructureWords = []
        companyStructureWords = companyStructureWords + ['THE', ' LIMITED', ' LTD', ' COMPANY', ' FUND', ' CORPORATION', ' PLC']
        companyStructureWords = companyStructureWords + [' HOLDINGS', ' GROUP', ' INCORPORATED', ' CONSOLIDATED', ' ENTERPRISES']
        companyStructureWords = companyStructureWords + [' STAPLED', ' NZX', ' NZ', ' CO.', ' FORUS', ' TRUST']

        businessAreaWords = []
        businessAreaWords = businessAreaWords + [' MINING', ' PETROLEUM', ' COMMUNICATIONS', ' SERVICES', ' RESOURCES', ' MINERALS']
        businessAreaWords = businessAreaWords + [' ENTERTAINMENT', ' PROPERTY', ' MINERAL', ' HEALTHCARE', ' HEALTH CARE', ' INVESTMENTS']
        businessAreaWords = businessAreaWords + [' AIRWAYS', ' AIR WAYS', ' LEISURE', ' ENERGY', ' TRAVEL', ' METALS', ' COAL', ' BANKING']
        businessAreaWords = businessAreaWords + [' MEDIA', ' BUILDING', ' TELECOM', ' HEALTH', ' INVESTMENT', ' MANAGEMENT', ' METAL']
        businessAreaWords = businessAreaWords + [' PHARMACEUTICALS', ' ASSET', ' FINANCIAL', ' ROADS', ' INDUSTRIES', ' PROPERTIES']
        businessAreaWords = businessAreaWords + [' LIFESTYLE', ' RESORTS', ' STEEL', ' WASTE', ' RETAIL', ' MEDICAL', ' TELEVISION']
        businessAreaWords = businessAreaWords + [' MORTGAGE', ' INSURANCE', ' ADMINISTRATION', ' CARE', ' PHARMACEUTICAL', ' AGRICULTURAL']
        businessAreaWords = businessAreaWords + [' ORD UNITS', ' OUTDOOR', ' NEWS']

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


            companyInfo[index].companyNameModified = self._stripNames(companyInfo[index].companyNameModified)
            companyInfo[index].removedWords        = self._stripNames(companyInfo[index].removedWords)
            companyInfo[index].businessArea        = self._stripNames(companyInfo[index].businessArea)
            companyInfo[index].location            = self._stripNames(companyInfo[index].location)
            
            
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

    #Plan of attack
    # compare each name to each company. For each company,
    # compare the name to the company name, company name plus business area, company aliases and company people
    # The metric for similarity is the jaccard index. 
    # The comparison with the minimum jaccard index is taken to represent the comparison between the company and the name. 
    def _matchCompanyToName(self, names):
        companyCodes = []
        companyConfidences = []
        companyNames = []
        for name in names:
            name = self._stripNames(name)
            for index in range(len(self.companyInfo)):
                
                companyName = self.companyInfo[index].companyNameModified
                nameBusinessArea = companyName + self.companyInfo[index].businessArea
                
                nameDist = jaccard_distance(set(list(name)), set(list(companyName)))
                nameBusinessAreaDist = jaccard_distance(set(list(name)), set(list(nameBusinessArea)))

                # alias match is the maximum match of all listed aliases
                if len(self.companyInfo[index].aliases)>0:
                    aliases = self.companyInfo[index].aliases.split('_')
                    aliasDists = []
                    for alias in aliases:
                        aliasDists.append(jaccard_distance(set(list(name)), set(list(alias))))
                    aliasDist = min(aliasDists)
                else:
                    aliasDist = 1

                # people match is the maximum match of all listed names. 
                if len(self.companyInfo[index].people)>0:
                    people = self.companyInfo[index].people.split('_')
                    peopleDists = []
                    for person in people:
                        peopleDists.append(jaccard_distance(set(list(name)), set(list(person))))
                    peopleDist = min(peopleDists)
                else:
                    peopleDist = 1

                companyMatch = 1- min([nameDist, nameBusinessAreaDist, aliasDist, peopleDist])

                if companyMatch > 0.7:
                    #print '     ', companyName, ' _ ', nameBusinessArea
                    #print '     ', str(1-nameDist), ' _ ', str(1-nameBusinessAreaDist), ' _ ', str(1-aliasDist)
                    companyCodes.append(self.companyInfo[index].asxCode)
                    companyConfidences.append(companyMatch)
                    companyNames.append(self.companyInfo[index].companyName)


        return companyCodes, companyConfidences, companyNames

# Level 2
    # Remove all instances of the words contained in the wordsToRemoveList
    # Store the removed words in removedWords, store the remainder in name
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

    # Convert string to uppercase, remove spaces and remove punctuation
    def _stripNames(self, name):
        name.translate(None, string.punctuation)
        name = name.upper().replace(' ', '')
        return name

#Main
if __name__ == "__main__":
    headlineparser = HeadlineParser('20161201-asx200.csv')

    dateString = '01_Jan_2016'
    headlineList = ["Explosion in Bluescope factory linked to operational defects.", "Apn outdoor takes lion's share of merger", "4 dead on Dreamworld ride.", "Commbank loses out big on shaky investments", "Woodside closes slightly down on weak exports", "Ardent CEO to address Dreamworld tragedy", "Andrew Wood dead at 65", "Peter Meurs has given up a job managing Fortescue's $US9.2 billion expansion project to pursue his true passion"]

    for line in headlineList:
        print ''
        print line
        resultList = headlineparser.parseHeadline(line, dateString)
        for result in resultList:
            print result.companyCode + '  ' + str(result.sentiment) + '   ' + str(result.confidenceOfCode) + '  ' + result.companyName
