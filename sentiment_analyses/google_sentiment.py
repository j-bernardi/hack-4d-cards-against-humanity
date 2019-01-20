from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def GCP(quote):
    client = language.LanguageServiceClient.from_service_account_json('PATH TO JSON')
    document = types.Document(content=quote, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment.score
