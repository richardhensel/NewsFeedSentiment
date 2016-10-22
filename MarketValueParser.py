

# A container class for storing company names information. 
class CompanyValues():
    def __init__(self, csvRow):
        self.companyCode = csvRow[0]
        self.date        = csvRow[1]
        self.openPrice   = csvRow[2]
        self.highPrice   = csvRow[3]
        self.lowPrice    = csvRow[4]
        self.closePrice  = csvRow[5]
        self.volume      = csvRow[6]

class ValueParser():

    def __init__ (self, companyNamesPath):
        self.companyNames = []


    def readValueFile(self, valueFilePath):
        print('Importing company value data...')
        with open(os.path.join(valueFilePath)) as localfile:
            reader = csv.reader(localfile,delimiter=',',quotechar='"')
            reader.next()
            for row in reader:
                self.companyNames.append(CompanyNames(row))

