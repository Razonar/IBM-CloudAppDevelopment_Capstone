import requests
import json
from . models import CarModel, CarDealer, CarMake, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    #print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    #print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json = json_payload)
    status_code = response.status_code
    #print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        #print(json_result)
        dealers = json_result["body"]
        # Get its content in `doc` object
        #print(dealers["docs"])
        dealer_doc = dealers["docs"][0]
        #print(dealer_doc)
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
        

    return dealer_obj

def get_dealer_review_from_cf(url, **kwargs):
    results=[]
    #print(kwargs)
    dealer_id = kwargs['id']
    #print(dealer_id)
    json_result = get_request(url, id = dealer_id)
    #print(json_result)
    if json_result:
        #print(json_result["body"]["data"]["docs"])
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            #print(review)
            if review['purchase'] == True or review['purchase'] == 'true':
                            review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date=review["purchase_date"], review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                            results.append(review_obj)
                            #print(review_obj)
            else:
                            review_obj = DealerReview(car_make='None', car_model='No car',
                                    car_year=0, dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date='', review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                            results.append(review_obj)
                            #print(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/4c560162-62ac-433a-b774-537e51bf266d"
    api_key = "xxx"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    #print(text)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return label
