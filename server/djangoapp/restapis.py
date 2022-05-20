import requests
import json
import logging
# import related models here
from requests.auth import HTTPBasicAuth
from . import models
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    json_data={}
    try:
        # Call get method of requests library with URL and parameters
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)

    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, json_payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data


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
        dealers = json_result['dealerships']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = models.CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                          id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                          short_name=dealer["short_name"], state=dealer["state"],
                                          st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_reviews_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])

            if  review["purchase"] is False:
                review_obj = models.DealerReview(id=review["id"], name=review["name"],
                                                 dealership=review["dealership"], review=review["review"], purchase=review["purchase"],
                                                 purchase_date='none', car_make='none',
                                                 car_model='none', car_year='none', sentiment="none")
                print(review_obj.sentiment)
                results.append(review_obj)

            else:
                review_obj = models.DealerReview(id=review["id"], name=review["name"],
                                                 dealership=review["dealership"], review=review["review"], purchase=review["purchase"],
                                                 purchase_date=review["purchase_date"], car_make=review['car_make'],
                                                 car_model=review['car_model'], car_year=review['car_year'], sentiment=sentiment)

                print(review_obj.sentiment)
                results.append(review_obj)
        return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or


def analyze_review_sentiments(review):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/00ec2835-7f25-4e25-85de-b5c74650359d"
    apikey = "xxx"

    authenticator = IAMAuthenticator(apikey)
    nlu = NaturalLanguageUnderstandingV1(version='2022-03-20',authenticator=authenticator)

    nlu.set_service_url(url)
    
    json_result = nlu.analyze(
        text=review,
        features=Features(sentiment=SentimentOptions()),
        return_analyzed_text=True
    ).get_result()

    sentiment = json_result['sentiment']['document']['label']
    return sentiment

#Call reviews db and return count of reviewsdict
def get_reviews_count(url):
    json_result = get_request(url)
    print(json_result["numReviews"])
    return json_result["numReviews"]
