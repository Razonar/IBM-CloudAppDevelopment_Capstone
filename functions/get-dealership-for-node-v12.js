// IBM Action, method=GET, node.js v12
// API https://4ea3b251.us-south.apigw.appdomain.cloud/api (for node v16)
// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

const Cloudant = require('@cloudant/cloudant'); 

function main(params) {

    secret={
    "COUCH_URL": "https://ab9a3133-c458-4795-8041-55b2ad164a33-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "Um1oyQP-JDmtWBQc90jbhv1EEz2-VgjSqkK-RIcpOkZe",
    "COUCH_USERNAME": "ab9a3133-c458-4795-8041-55b2ad164a33-bluemix"}

    return new Promise(function (resolve, reject) {
    const cloudant = Cloudant({
        url: secret.COUCH_URL,
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
    });
    const dealershipDb = cloudant.use('dealerships');

    if (params.state) {
        // return dealership with this state 
        dealershipDb.find({
            "selector": {
                "state": {
                    "$eq": params.state
                }
            }
        }, function (err, result) {
            if (err) {
                reject(err);
            }
            let code = 200;
            if (result.docs.length == 0) {
                code = 404;
            }
            resolve({
                statusCode: code,
                headers: { 'Content-Type': 'application/json' },
                body: result
            });
        });
    } else if (params.id) {
        id = parseInt(params.dealerId)
        // return dealership with this state 
        dealershipDb.find({ selector: { id: parseInt(params.id) } }, function (err, result) {
            if (err) {
                reject(err);
            }
            let code = 200;
            if (result.docs.length == 0) {
                code = 404;
            }
            resolve(
                {
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result
                });
        });
    } else {     // return all documents 
        dealershipDb.list({ include_docs: true }, function (err, result) {
            if (err) {
                reject(err);
            }
            resolve({
                statusCode: 200,
                headers: { 'Content-Type': 'application/json' },
                body: result
            });
        });
    }
});
   
};
