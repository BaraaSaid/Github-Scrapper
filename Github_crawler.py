#Get the data
#don't forget to consider lowecasing keywords as well as github menu items
from bs4 import BeautifulSoup
import requests
import json
import pprint
import random 
import sys

basic_url = "https://github.com"
protcol_type = ['http', 'https']

def random_choice(items):
    """
    Returns a random item from the given list items.
    """
    return (random.choice(items))

def read_json(input_file):
    """
    Reads a json file and returns the data it contains.
    """
    with open(input_file, mode='rb') as json_file:
        data = json.load(json_file)
        return data
    

def parse_data(json_data, url_fragment):
    """
    Parses a dictionary and returns the data related to the specific url fragment /
    we attempt to create in the query.
    """
    return json_data[url_fragment]

def query_fragment(search_terms_list):
    """
    Given the search terms list, this function returns the query part of the url.
    """
    search_query = ''
    for search_term in search_terms_list :
        search_term.lower()
        search_query += search_term +'+' 
    return search_query[:-1]

def construct_search_url(json_data):
    """
    Given the input json file, this functions constructs the search url that'll be used to request\
    the internet browser.  
    """
    search_terms_list = parse_data(json_data, 'keywords')
    search_query = query_fragment(search_terms_list)
    query_type = parse_data(json_data, 'type')
    search_url = basic_url + '/search?q=' + search_query + '&type=' + query_type

    return search_url

def create_proxy(json_data):
    """
    Using the json input, this function returns the dictionary mapping protocol to the URL of \
    the proxy.
    """
    
    proxies_list = parse_data(json_data, 'proxies')
    proxy_dict = {}
    proxy = random_choice(proxies_list)
    proxy_dict['http'] = proxy
    proxy_dict['https'] = proxy

    return proxy_dict

def request_url(url, proxy_dict):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    request, otherwise return None.
    """
    try:
        resp = requests.get(url, proxies =proxy_dict )
        return resp
    except Exception as err:
        raise Exception(str(err))


#Parse data

def parse_html(resp):
    """
    Parses the html using beautiful soup, stores it in variable `soup` and returns it, \
    given the response of the url request. 
    """
    try :

        soup = BeautifulSoup(resp.text, "lxml")
        return soup
    except Exception as err:
        raise Exception(str(err))

def find_url(soup, github_menu_item):
    """
    returns a list of dictionaries mapping the urls associated with the keywords and the github
    menu item given in the json input file. 
    """
    url_list = []
    github_menu_item = github_menu_item.replace(' ', '').lower()
    
    if github_menu_item == 'repositories' :
        repositories = soup.select('ul.repo-list > div > div > h3 > a')
        for repository in repositories :
            url_dict = {}
            url_dict["url"] = basic_url + repository['href']
            url_list.append(url_dict)
        return url_list
    
    elif github_menu_item == 'issues' :
        issues = soup.select('div#issue_search_results > div.issue-list \
        div.issue-list-item.col-12.py-4 h3 a')
        for issue in issues :
            url_dict = {}
            url_dict["url"] = basic_url + issue['href']
            url_list.append(url_dict)
        return url_list
    
    elif github_menu_item == 'wikis':
        wikies = soup.select('div#wiki_search_results > div.wiki-list > \
        div.wiki-list-item a.h5')
        for wiki in wikies :
            url_dict = {}
            url_dict["url"] = basic_url + wiki['href']
            url_list.append(url_dict)
        return url_list

#output the data

def output_json_object(url_list):
    """
    returns json object of the list found urls related to the query
    """
    json_output = json.dumps(url_list, separators=(',',':'))
    return json_output


def is_argument_missing(arguments):
    """
    Checks if the input json file exist, otherwise stops process.
    """

    if arguments < 2 :
        raise Exception('Missing arguments , at least 1 required argument ')

def crawl_website(data):
    url = construct_search_url(data)
    proxy_dict = create_proxy(data)
    resp = request_url(url, proxy_dict)
    soup = parse_html(resp)
    github_menu_item = parse_data(data, 'type')
    url_list = find_url(soup, github_menu_item)

    return url_list
   

def main():
    try :
        arguments = len(sys.argv)
        is_argument_missing(arguments)
        input_file = sys.argv[1]
        data = read_json(input_file)
        url_list = crawl_website(data)
        json_url_list = output_json_object(url_list)
        pprint.pprint(json_url_list)
    except :
        pprint.pprint('Fatal Error')

        

if __name__ == '__main__':
    main()











            







