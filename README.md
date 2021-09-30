# News Sentiment Analysis

News Sentiment Analysis is a tool to scrape and analyse the sentiment of financial news scraped from the web.
Sentiment analysis is done using Google's Cloud Natural Language API.

## Initialisation
1) Ensure all five modules are present in the same directory:  
    main.py  
    Ui.py  
    Data.py  
    Parse.py  
    Analysis.py  

2) If articles have been pre-downloaded, ensure that articles.csv is also present in the same directory. Else, articles can be downloaded with Data.py module.

3) Ensure that Google's Cloud Natural Language API is accessible by setting the application credentials variable in Analysis.py:
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key.json
```
## Main Usage
All modules have been packaged into a single file, main.exe. Following the instructions on the GUI would yield the proper analysis results.


## Alternative usage

```python
# Data() object checks if articles.csv is present at initialisation. If not present, it proceeds to scrape articles from the web.
data = Data()

# returns articles relating to a company.
parse = Parse(company=company)
parse.get_articles_of_interest()

# analyses one article using Google's Cloud Natural Language API. Articles are stored in the Analysis object, indexed by integers [0, number of articles)
analysis = Analysis(company=company, data=articles_of_interest, size=number_of_articles)
analysis.analyse(index)
    
# prints the sentiment analysis
analysis.show_analysis()
```

## Known Issues
The use of PySimpleGUI as the GUI manager breaks abstraction between the Ui.py module and main module, making the code messy.
