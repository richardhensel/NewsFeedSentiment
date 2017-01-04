import sqlite3

class Databaser:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.curs = self.conn.cursor()

        try:
            self.createTables() 
        except:
            print 'Databaser: Error creating tables, maybe already exists'

    def createTables(self):
        # Create Application table.
        s  = 'CREATE TABLE Headline ('
        s += 'timestamp               text,'
        s += 'companyCode             text,'
        s += 'confidenceOfCode        text,'
        s += 'sentiment               text,'
        s += 'companyName             text,'
        s += 'keywordList             text'
        s += ')'

        self.curs.execute(s)

    def addRow(self, headlineResult):
        
        # Add to Applications table.
        s  = 'INSERT INTO Headline VALUES(' 
        s += '"' + str(headlineResult.timestamp)            + '"' + ','
        s += '"' + str(headlineResult.companyCode)          + '"' + ','
        s += '"' + str(headlineResult.confidenceOfCode)     + '"' + ','
        s += '"' + str(headlineResult.sentiment)            + '"' + ','
        s += '"' + str(headlineResult.companyName)          + '"' + ','
        s += '"' + str(headlineResult.keywordList)          + '"'
        s += ')'

        self.curs.execute(s)
        self.conn.commit()

    def close(self):
        self.conn.close()
