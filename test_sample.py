import Github_crawler
import pytest
import validators
from collections import OrderedDict

def test_random_choice():
    cities = ['Tunis', 'Ariana', 'Sfax', 'Sousse']
    for i in range(len(cities)*10):
        assert Github_crawler.random_choice(cities) in cities

def test_read_json():
    with open('test_file', 'w') as input_file :
        input_file.write('{"keywords": ["openstack","nova","css"],\
    "proxies": [null],\
    "type": "Repositories"}')

    assert Github_crawler.read_json("test_file") == {'keywords': ['openstack','nova'\
    ,'css'],\
    'proxies': [None],\
    'type': 'Repositories'}

def test_parse_data() :
    json_data = {'keywords': ['openstack','nova','css'],\
    'proxies': [None],\
    'type': 'Repositories'}
    assert Github_crawler.parse_data(json_data, 'keywords') == ['openstack','nova',\
    'css']

def test_read_unexistant_json():
    with pytest.raises(FileNotFoundError):
        Github_crawler.read_json('datta.json')

def test_parse_unexistant_keyword():
    json_data = {'keywords': ['openstack','nova','css'],\
    'proxies': [None],\
    'type': 'Repositories'}
    with pytest.raises(KeyError):
        Github_crawler.parse_data(json_data, 'commit')

def test_query_fragment():
    assert Github_crawler.query_fragment(['openstack', 'nova', 'css']) == \
    'openstack+nova+css'

def test_construct_search_url():
    json_data = {'keywords': ['openstack','nova','css'],\
    'proxies': ['89.23.19.143', '43.239.73.30'],\
    'type': 'Repositories'}
    url = Github_crawler.construct_search_url(json_data)

    assert validators.url(url) == True

def test_create_proxy():
    json_data = {'keywords': ['openstack','nova','css'],\
    'proxies': ['89.23.19.143', '43.239.73.30'],\
    'type': 'Repositories'}
    proxy_dict = Github_crawler.create_proxy(json_data)
    assert (proxy_dict['http'] and proxy_dict['https'] )in \
    ['89.23.19.143', '43.239.73.30']  

def test_request_url():
    assert Github_crawler.request_url("https://github.com/search?q=openstack+nova+css\
    &type=Repositories", {'http':'43.239.73.30'}).status_code == 200

def test_find_url_repositories():
    resp = Github_crawler.request_url("https://github.com/search?q=openstack+nova+css\
    &type=Repositories", {'http':'13.78.125.167:8080'})
    soup = Github_crawler.parse_html(resp)
    urls = Github_crawler.find_url(soup, 'Repositories', {'http':'13.78.125.167:8080'})
    for url in urls :
        assert type(url) == OrderedDict
        assert len(url) == 2
        assert set(url.keys()) == {'extra', 'url'}
        assert validators.url(url['url'])
    

def test_find_url_issues():
    resp = Github_crawler.request_url("https://github.com/search?q=openstack+nova+css\
    &type=Issues", {'http':'13.78.125.167:8080'})
    soup = Github_crawler.parse_html(resp)
    urls = Github_crawler.find_url(soup, 'Issues', {'http':'13.78.125.167:8080'})
    for url in urls :
        assert validators.url(url['url'])
    

def test_find_url_wikis():
    resp = Github_crawler.request_url("https://github.com/search?q=openstack+nova+css\
    &type=Wikis", {'http':'13.78.125.167:8080'})
    soup = Github_crawler.parse_html(resp)
    urls = Github_crawler.find_url(soup, 'Wikis', {'http':'13.78.125.167:8080'})
    for url in urls :
        assert validators.url(url['url'])
    

def test_is_argument_missing():
    arguments = len(['arg1'])
    with pytest.raises(Exception) as except_info :
        Github_crawler.is_argument_missing(arguments )
        assert str(except_info.value.message) == 'Missing arguments , at least 1 \
        required argument '

def test_is_argument_non_missing():
    arguments = len(['arg1', 'arg2'])
    assert Github_crawler.is_argument_missing(arguments) is None


def test_read_json_and_construct_search_url():
    with open('test_file', 'w') as input_file :
        input_file.write('{"keywords": ["openstack","nova","css"],\
    "proxies": ["89.23.19.143", "43.239.73.30"],\
    "type": "Repositories"}')
    input_data = Github_crawler.read_json('test_file')
    url = Github_crawler.construct_search_url(input_data)

    assert validators.url(url)

def test_output_json_object():
    json_test = '[{"test":"valid"},{"function":"output_json_object"}]'
    list_test = [{'test':'valid'},{'function':'output_json_object'}]
    assert Github_crawler.output_json_object(list_test) == json_test

def test_extra_crawling():
    proxy_dict = {'http' : '213.222.34.200:53281', 'https' : '213.222.34.200:53281'}
    url_repo = "https://github.com/atuldjadhav/DropBox-Cloud-Storage"
    extra_dict = Github_crawler.extra_crawling(url_repo, proxy_dict)
    keys = extra_dict.keys()
    assert type(extra_dict) == OrderedDict
    assert len(extra_dict) == 2 
    assert set(keys) == {'owner', 'language_stats'}
    assert type(extra_dict['language_stats']) == OrderedDict
    for key in extra_dict['language_stats'] :
        assert (type(key) == str and type(extra_dict['language_stats'][key]) == float \
        and (extra_dict['language_stats'][key] > 0) and\
        (extra_dict['language_stats'][key] <= 100)) == True

def test_main():
    with open('test_file', 'w') as input_file :
        input_file.write('{"keywords": ["openstack","nova","css"],\
    "proxies": ["95.182.97.96:53281", "59.152.13.101:8080"],\
    "type": "Repositories"}')
    input_data = Github_crawler.read_json('test_file')
    url_list = Github_crawler.crawl_website(input_data)
    for url in  url_list :
        assert validators.url(url['url'])















