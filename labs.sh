# Labs console commands

# Lab 1
#######################################

git clone https://github.com/Razonar/IBM-CloudAppDevelopment_Capstone
cd IBM-CloudAppDevelopment_Capstone/server
pip3 install -r requirements.txt

# Delete "db.sqllite3".
python3 manage.py makemigrations 
python3 manage.py migrate --run-syncdb
# or python3 manage.py migrate 

python3 manage.py createsuperuser

# Launch Application with port server 8000
# add the /djangoapp to the path
python3 manage.py runserver

ibmcloud login --no-region -u mathcalc@msn.com
ibmcloud account orgs
ibmcloud target --cf-api https://api.REGION.cf.cloud.ibm.com -r REGION -o ACCOUNTOWNER
ibmcloud cf install

# Create the space only the first time
# ibmcloud account space-create djangoserver-space

# Target
ibmcloud target -s djangoserver-space

# manifest.yml
# Defines two applications: djangoapp and djangoapp-nginx
# Can but better not, change the names.
# append the host using the route entry to ALLOWED_HOSTS
ibmcloud cf domains

# djangobackend/settings.py
# Specify $HOST.$DOMAIN with the previous values
    
# Deploy
ibmcloud cf push

# Lab 2: User Management
#######################################

git clone https://github.com/Razonar/IBM-CloudAppDevelopment_Capstone
cd IBM-CloudAppDevelopment_Capstone/server
pip3 install -r requirements.txt

# Launch at 8000 and as superuser
# add /admin and log with root@pwd created
python3 manage.py createsuperuser
python3 manage.py runserver

# Lab 3: Implement IBM Cloud Function Endpoints
#######################################

git clone https://github.com/Razonar/IBM-CloudAppDevelopment_Capstone
cd IBM-CloudAppDevelopment_Capstone/server
pip3 install -r requirements.txt

npm install -g couchimport
export IAM_API_KEY="REPLACED IT WITH GENERATED `apikey`"
export COUCH_URL="REPLACED IT WITH GENERATED `url`"
cd cloudant/data
npm install -g couchimport

cat ./dealerships.json | couchimport --type "json" --jsonpath "dealerships.*" --database dealerships
cat ./reviews.json | couchimport --type "json" --jsonpath "reviews.*" --database reviews

couchimport


# Lab 5: Containerize your application
#######################################


