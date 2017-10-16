# -*- coding: utf-8 -*-
"""
Yelp Fusion API 

Taken from the code sample located at: https://github.com/Yelp/yelp-fusion/tree/master/fusion/python
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import csv
import pandas as pd
from creds import bearer_token, client_id, client_secret


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = client_id
CLIENT_SECRET = client_secret


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
# DEFAULT_TERM = 'restaurant'
# DEFAULT_LOCATION = 'Brooklyn, NY'
# SEARCH_LIMIT = 1
json_output = open('yelp_restaurants.json', 'w+')

def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = bearer_token
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    
    
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(bearer_token, business_id)

   # print(u'Result for business "{0}" found:'.format(business_id))
    #pprint.pprint(response, indent=2)
    
    business_name = businesses[0]['name']
    business_rating = businesses[0]['rating']
    business_price = businesses[0]['price']
    business_review_count = businesses[0]['review_count']
    business_is_closed = businesses[0]['is_closed']
    business_categories = businesses[0]['categories']
    
    return business_id,business_name,brating,bprice,breview_count,bis_closed,bcategories
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        business_id,business_name,business_rating,business_price,business_review_count,business_is_closed,business_categories =  query_api(input_values.term, input_values.location)

        yelp_dict = {}
        yelp_dict['business_id'] = business_id
        yelp_dict["business_name"] = business_name
        yelp_dict['rating'] = business_rating
        yelp_dict['price'] = business_price
        yelp_dict['review_count'] = business_review_count
        yelp_dict['is_closed'] = business_is_closed
        yelp_dict['categories'] = business_categories
        #query_api(input_values.term, input_values.location)
         
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

    print (json.dumps(yelp_dict, sort_keys=True, indent=2))
    json.dump(yelp_dict, json_output)
    json_output.write("\n")
    
names = []
loc = []
i = 0
df = pd.read_csv('search.csv')

if __name__ == '__main__':
    #main()
    for i in range(len(df)):
        names.append(df['name'][i])
        loc.append(df['address'][i])

    for i in range(len(names)):
        DEFAULT_TERM = names[i]
        print(DEFAULT_TERM,loc[i])
        DEFAULT_LOCATION = loc[i]
        SEARCH_LIMIT = 1
        API_HOST = 'https://api.yelp.com'
        SEARCH_PATH = '/v3/businesses/search'
        BUSINESS_PATH = '/v3/businesses/'

        try:
            main()

        except:
            pass





