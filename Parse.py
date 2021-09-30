import os
import pandas as pd


class Parse:

    MINIMUM_LENGTH = 50

    URL = "url"
    CONTENT = "content"
    CSV_NAME = "articles.csv"
    REGEX = "(?i)"

    def __init__(self, company=None):
        self.company = company.strip(" ")
        if os.path.isfile(self.CSV_NAME):
            data = self.get_csv()
            self.set_data(data)
        else:
            print("Call Data() object before calling Parse().")
            self.data = None

    def get_data(self):
        return self.data

    def get_csv(self):
        if os.path.isfile(self.CSV_NAME):
            df = pd.read_csv(self.CSV_NAME, index_col=False, low_memory=False)
            df = df[[self.URL, self.CONTENT]]
            df = df.dropna()
            df = df[df[self.CONTENT].str.len() >= self.MINIMUM_LENGTH]
            df.reset_index(inplace=True, drop=True)
            return df
        else:
            return None

    def get_articles_of_interest(self):
        if self.company:
            if self.data is not None:
                data = self.data[self.data[self.CONTENT].str.contains(self.REGEX + self.company)]
                data.reset_index(inplace=True, drop=True)
                self.set_data(data)
                return data
            print("Make sure you call Data() before calling Parse().")
            return None
        print("You didn't key in a company when calling Parse(). Try calling Parse(company=COMPANY_NAME).")
        return None

    def set_data(self, data):
        self.data = data

    def get_len_articles_of_interest(self):
        if self.data is not None:
            return len(self.data)
        else:
            return 0