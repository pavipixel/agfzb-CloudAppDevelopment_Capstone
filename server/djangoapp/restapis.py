import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1
    import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_state_from_cf(url, state):

    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):

    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        reviews_list = json_result["entries"]
        # For each review object
        for review in reviews_list:
            # Get its content in `doc` object
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(id=review["id"], name=review["name"], dealership=review["dealership"],
                                   purchase=review["purchase"], car_make=review["car_make"], car_model=review["car_model"],
                                   car_year=review["car_year"], review=review["review"], purchase_date=review["purchase_date"], sentiment=" ")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    apikey = 'joCkd7IA8AO1L7HvQEuZdUW0fqxW53DeDgcwLhWmKFq4'
    apiurl = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8cefc3ae-b857-4276-b939-f81713b59e98'

    authenticator = IAMAuthenticator('{apikey}')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator 
    )

    natural_language_understanding.set_service_url('{apiurl}')

    response = natural_language_understanding.analyze(
        text= text,
        features=Features(sentiment=SentimentOptions(targets=['bonds']))).get_result()

    # - Get the returned sentiment label such as Positive or Negative
    if response:
        senti = response["sentiment"]
        doc = senti["document"]
        return doc["label"]



