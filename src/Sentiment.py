from textblob import TextBlob

class Analysis():
    def __init__(self, text):
        self.blob = TextBlob(text)
        return self.blob
