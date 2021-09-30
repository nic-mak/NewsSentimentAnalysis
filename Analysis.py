import os
from google.cloud import language_v1


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/nicho/PycharmProjects/GreensillNewsSentiment/news-sentiment-analysis-298506-4b324571affe.json"


class Analysis:

    RESULTS = "results"
    CONTENT = "content"
    SENTIMENT = "sentiment"
    MAGNITUDE = "magnitude"

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    WEAK = "weak"
    STRONG = "strong"
    ALL = "all"

    def __init__(self, company=None, data=None, size=None):
        self.company = company
        self.data = data
        self.size = size

    def get_data(self):
        return self.data

    def get_percentages(self):
        sentiments = self.count_sentiments(self.ALL)
        sentiments_positive = self.count_sentiments(self.POSITIVE)
        sentiments_negative = self.count_sentiments(self.NEGATIVE)
        sentiments_neutral = self.count_sentiments(self.NEUTRAL)

        sentiments_percentage_positive = self.get_percentage(sentiment=sentiments_positive, total=sentiments)
        sentiments_percentage_negative = self.get_percentage(sentiment=sentiments_negative, total=sentiments)
        sentiments_percentage_neutral = self.get_percentage(sentiment=sentiments_neutral, total=sentiments)

        return sentiments_percentage_positive, sentiments_percentage_negative, sentiments_percentage_neutral

    def get_percentage(self, sentiment, total):
        return sentiment / total * 100

    def get_average_magnitudes(self):
        magnitude_average_positive = self.get_average_magnitude(sentiment=self.POSITIVE)
        magnitude_average_negative = self.get_average_magnitude(sentiment=self.NEGATIVE)
        magnitude_average_neutral = self.get_average_magnitude(sentiment=self.NEUTRAL)

        return magnitude_average_positive, magnitude_average_negative, magnitude_average_neutral

    def get_average_magnitude(self, sentiment):
        data = self.get_data()
        if sentiment == self.POSITIVE:
            return data[data[self.SENTIMENT] > 0][self.MAGNITUDE].mean()

        elif sentiment == self.NEGATIVE:
            return data[data[self.SENTIMENT] < 0][self.MAGNITUDE].mean()

        elif sentiment == self.NEUTRAL:
            return data[data[self.SENTIMENT] == 0][self.MAGNITUDE].mean()

    def get_average_magnitude_category(self, magnitude):
        if magnitude == 0:
            return self.NEUTRAL
        elif magnitude < 5:
            return self.WEAK
        elif magnitude > 10:
            return self.STRONG

    def set_data(self, data):
        self.data = data

    def clean_data(self):
        data = self.get_data()
        new_data = data[data[self.SENTIMENT].notna()]
        number_of_articles_removed = len(data) - len(new_data)
        if number_of_articles_removed > 1:
            print(f"{number_of_articles_removed} articles were rejected due to its contents.")

        self.set_data(new_data)

    def analyse(self, index):
        client = language_v1.LanguageServiceClient()
        data = self.get_data()
        sentence = data.iloc[[index]][self.CONTENT].to_string()
        document = language_v1.Document(content=sentence, type_=language_v1.Document.Type.PLAIN_TEXT)

        try:
            print("Analysing " + str(index + 1) + " out of " + str(self.size) + " articles.")
            annotations = client.analyze_sentiment(document=document)
            score = annotations.document_sentiment.score
            magnitude = annotations.document_sentiment.magnitude
            data.at[index, self.SENTIMENT], data.at[index, self.MAGNITUDE] = score, magnitude
        except:
            data.at[index, self.SENTIMENT], data.at[index, self.MAGNITUDE] = None, None

    def count_sentiments(self, sentiment):
        data = self.get_data()
        if sentiment == self.POSITIVE:
            return len(data[data[self.SENTIMENT] > 0])

        elif sentiment == self.NEGATIVE:
            return len(data[data[self.SENTIMENT] < 0])

        elif sentiment == self.NEUTRAL:
            return len(data[data[self.SENTIMENT] == 0])

        else:
            return len(data)

    def show_analysis(self):
        if not self.data.empty:
            self.clean_data()
            sentiments_percentage_positive, sentiments_percentage_negative, sentiments_percentage_neutral = self.get_percentages()
            magnitude_average_positive, magnitude_average_negative, magnitude_average_neutral = self.get_average_magnitudes()
            category_positive = self.get_average_magnitude_category(magnitude_average_positive)
            category_negative = self.get_average_magnitude_category(magnitude_average_negative)
            category_neutral = self.get_average_magnitude_category(magnitude_average_neutral)

            print(f"""
            {sentiments_percentage_positive:.1f}% of sentiments were positive
            The average magnitude of positive sentiments is {magnitude_average_positive:.1f}. 
            This shows that the positive sentiments were {category_positive}.
            
            {sentiments_percentage_negative:.1f}% of sentiments were negative
            The average magnitude of negative sentiments is {magnitude_average_negative:.1f}
            This shows that the negative sentiments were {category_negative}.
           
            {sentiments_percentage_neutral:.1f}% of sentiments were neutral
            The average magnitude of neutral sentiments is {magnitude_average_neutral:.1f}
            This shows that the neutral sentiments were {category_neutral}.
            """)
        else:
            print("There are no relevant articles related to this company.")