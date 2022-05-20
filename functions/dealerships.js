// IBM Action, method=GET, node.js v12
// API  https://4ea3b251.us-south.apigw.appdomain.cloud/dealerships
// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

const Cloudant = require('@cloudant/cloudant'); 

async function main(params) { 

    secret={
    "COUCH_URL": "https://ab9a3133-c458-4795-8041-55b2ad164a33-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "Um1oyQP-JDmtWBQc90jbhv1EEz2-VgjSqkK-RIcpOkZe",
    "COUCH_USERNAME": "ab9a3133-c458-4795-8041-55b2ad164a33-bluemix"}

    const cloudant = Cloudant({ 
        url: secret.COUCH_URL, 
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } } 
    }); 
    let dbListPromise = await getDbs(cloudant); 
    return dbListPromise; 
} 

function getDbs(cloudant) { 
    return new Promise((resolve, reject) => { 
        let db = cloudant.use('dealerships'); 
        let result = db.list( {fields : ['id','city','state','st','address','zip','lat','long','short_name','full_name'],
        include_docs:true} ) 
            .then(result => { 
                resolve({ body: result}) 
            }) 
            .catch(err => { 
                reject({ err: err}); 
            }); 
    }); 
} 
