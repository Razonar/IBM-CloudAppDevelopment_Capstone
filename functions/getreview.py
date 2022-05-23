# IBM Action, method=GET, Python 3.9
# API https://4ea3b251.us-south.apigw.appdomain.cloud/getreview/getreview
# Params
# {
#     "id": 15
# }
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    # my IAM_API_KEY
    authenticator = IAMAuthenticator("Um1oyQP-JDmtWBQc90jbhv1EEz2-VgjSqkK-RIcpOkZe")
    service = CloudantV1(authenticator=authenticator)
    # my COUCH_URL
    service.set_service_url("https://ab9a3133-c458-4795-8041-55b2ad164a33-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
        db='reviews',
        selector={'dealership': {'$eq': int(dict["id"])}},
        ).get_result()
    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }
