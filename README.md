# Mobile_Service_API
A Mobile Service API that takes textual address via query parameters and returns the network coverage for available service providers

## Technologies used:
 - Django
 - Django REST Framework
 - Python
 
## API's used:
[API Adresse (https://adresse.data.gouv.fr/api-doc/adresse)](url "https://adresse.data.gouv.fr/api-doc/adresse")
Info: Get address details from a query address, including lon, lat and lambert93 coordinates

## Requirements:
Please install the following tools and technologies after cloning the project
- pip install django djangorestframework simplejson requests

## Usage:
This API only accepts GET requests

To make a GET request, use the port=8000
- The base API url will be something like = 'http://localhost:8000/api/
- Add your query parameters to the base url like this "http://localhost:8000/?q=8+bd+du+port"

