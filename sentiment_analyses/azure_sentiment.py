import requests, json

def azure_sentiment_score(quote):
    """Submits quote to Microsoft Azure for sentiment score"""
    quote_header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key
        }
    quote_payload = {
        "documents": [
            {
              "language": "en",
              "id": "1",
              "text": quote
            }
          ]
    }

    quote_response = requests.post("https://uksouth.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment",
        headers=quote_header, json=quote_payload)
    print(quote_response.json())
    if(quote_response.status_code == 200):
        print(quote_response.json()['documents'][0]['score'])
        return quote_response.json()['documents'][0]['score']

def get_api_key():

    with open('azure-api.txt', 'r') as api:
        api = api.read().striplines()

if __name__ == "__main__":

    score = azure_sentiment_score("Smelly fish fingers!")
