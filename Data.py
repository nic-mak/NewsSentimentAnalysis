import os
import csv
import pandas as pd
from multiprocessing import Pool, cpu_count

from newspaper.article import ArticleException
from newspaper import build, popular_urls, Config


class Data:

    INDEX_URL = 0
    INDEX_CONTENT = 1

    URL = "url"
    CONTENT = "content"
    CSV_NAME = "articles.csv"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
    LOCAL_URLS = ['https://www.straitstimes.com/', 'https://www.channelnewsasia.com/', 'https://www.todayonline.com/',
                  'https://www.businesstimes.com.sg/']

    def __init__(self):
        if os.path.isfile(self.CSV_NAME):
            print("CSV is downloaded.")
        else:
            self.csv_data = {self.URL: [], self.CONTENT: []}
            articles = self.get_articles()
            self.write_csv(articles)

    def get_urls(self):
        urls = popular_urls()
        for url in self.LOCAL_URLS:
            urls.append(url)
        return urls

    def get_article(self, url):
        try:
            papers = []
            config = self.get_config()
            articles = build(url, memoize_articles=False, config=config)
            for article in articles.articles:
                article.download()
                article.parse()
                papers.append((article.url, article.text))
            return papers
        except ArticleException:
            pass

    def get_articles(self):
        if os.path.isfile(self.CSV_NAME):
            return None
        urls = self.get_urls()
        pool = Pool(processes=(cpu_count() - 1))
        articles = pool.map(self.get_article, urls)
        return articles

    def get_config(self):
        user_agent = self.USER_AGENT
        config = Config()
        config.browser_user_agent = user_agent
        return config

    def get_data(self):
        return self.csv_data

    def set_csv_url(self, url):
        self.csv_data[self.URL].append(url)

    def set_csv_content(self, content):
        self.csv_data[self.CONTENT].append(content)

    def set_data(self, articles_data):
        for article_data in articles_data:
            if article_data:
                for article in article_data:
                    url = article[self.INDEX_URL]
                    content = article[self.INDEX_CONTENT]
                    self.set_csv_url(url)
                    self.set_csv_content(content)

    def write_csv(self, articles_data):
        self.set_data(articles_data)
        df = pd.DataFrame(self.csv_data)
        df.to_csv(self.CSV_NAME, index=False, quoting=csv.QUOTE_ALL)