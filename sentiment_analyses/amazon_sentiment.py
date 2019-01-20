import ujson, boto3, json

def AWS_SWAG(quote):

    api_key = get_api_key()

    comprehend = boto3.client(aws_access_key_id='AKIAJ3T2DNUIDYGLGHPQ',
                              aws_secret_access_key=api_key,
                              service_name='comprehend',
                              region_name='eu-west-1')

    return json.dumps(comprehend.detect_sentiment(LanguageCode='en',Text=quote)['SentimentScore'])

def get_api_key():
    with open('sentiment_analyses/amazon_api.txt', 'r') as api:
        api_key = api.read().strip()
    return api_key

if __name__ == "__main__":
    resp = AWS_SWAG("I hate you")
    print(resp)
    print(type(resp))
