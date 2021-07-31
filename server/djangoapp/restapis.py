import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url)) 
    try:
        if "apikey" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print("Inside - API Key")
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs["apikey"]))
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.content)
            return json_data
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occured")
    json_data = json.loads(response.text)
    return json_data


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
    doc =  {}
    # - Call get_request() with specified arguments
    apikey = 'XN818Vy1ipBkhq-uOF4Xaz5WpjVRX7S2lgfuv9CrfIN5'
    #apikey = 'chYaPHG-h0OlKt77B0Tgp9mHfAdTGruUMLWU7LEajwvv'
    apiurl = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/d0cc8052-83e4-4519-8f09-b731cbacec91'
   
    authenticator = IAMAuthenticator('apikey')
    print("Authenticator------")
    print(authenticator)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator 
    )
    print("Natural Language-----------------------")
    natural_language_understanding.set_service_url('apiurl')
    print("Natural Language Set service-----------------------")
    response = natural_language_understanding.analyze(
        text= text,
        features=Features(sentiment=SentimentOptions(targets=['bonds']))).get_result()
    print("Response ---")
    print(response)
    senti = response["sentiment"]
    doc = senti["document"]
    return doc["label"]






