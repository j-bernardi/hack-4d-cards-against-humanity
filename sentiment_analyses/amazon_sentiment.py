import ujson, boto3

def AWS_SWAG(quote):

    comprehend = boto3.client(aws_access_key_id='AKIAJ3T2DNUIDYGLGHPQ',
                              aws_secret_access_key=api_key,
                              service_name='comprehend',
                              region_name='eu-west-1')

    return comprehend.detect_sentiment(LanguageCode='en',Text=quote)['SentimentScore']

def get_api_key():
    with open('azure-api.txt', 'r') as api:
        api_key = api.read().striplines()
    return api_key
