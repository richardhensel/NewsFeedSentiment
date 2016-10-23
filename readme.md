News Feed Sentiment


The intent of this program is to gauge the sentiment of news headlines pertaining to a country or corporation listed on a stock exchange. 

The Program will be composed of the following components:

1. News headline parser.
    The news headline parser has three objectives.
    a. determine if a headline references a country or corporation.
    b. gauge te sentiment of the headline relating to that entity. 
    c. store this sentiment against the entity along with a date and time of article. 

    Todo: Use existing nltk named entity recognition to pull entity names. Clean the names from headline and clean the names listed in asx. Compare using edit distance methods. 



2. Headline scraper.
    The web scraper has one objective.
    a. trawl website, loading the headline which can then be passed into the headline parser. 

3. Market data scraper.
    The market data scraper pulls down historical stock exchange and currency data.
    an example of this is http://www.asxhistoricaldata.com/
 
5. Where the magic happens. 
    The market analyser utilizes a learning algorithm such as regression to establish a correlation between news sentiment and a change in market value. 
