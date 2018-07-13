# Github-Scrapper
- The GitHub crawler returns all the links related to a github search given specific search terms, list of proxies and the type of the object we're looking for (Repositories, Issues and Wikis).

# Overview

- The crawling script is written in Python3. A version of python3.5+ is required to run this script.
- The unicode characters are supported by this script.

## Installation and Configuration :
- The required python packages for this project are stated in the file requirements.txt .
- The input file considered for this project is a JSON format file containing  the list of the search terms, as well as a list of proxies and the type of the github menu item we're looking for.

Below an example of the input file :

## Example of input file:

{
  "keywords": [
    "python",
    "django-rest-framework",
    "jwt"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}

Below an example of the output :

## Example of output file:

```json
[
  {
    "url": "https://github.com/GetBlimp/django-rest-framework-jwt"
  },
  {
    "url": "https://github.com/lock8/django-rest-framework-jwt-refresh-token"
  },
  {
    "url": "https://github.com/City-of-Helsinki/tunnistamo"
  },
  {
    "url": "https://github.com/chessbr/rest-jwt-permission"
  },
  {
    "url": "https://github.com/rishabhiitbhu/djangular"
  },
  {
    "url": "https://github.com/vaibhavkollipara/ChatroomApi"
  }
]
```
## Running the script

- The script can be run simply by this command python3 Github_crawler.py json_file
- A json file must be given as input file, otherwise, the script will raise an exception.
- The result will be printed into the standard output.

## Running tests

- The unit tests can be executed using this command:
py.test --cov=. .
Where  . is the location of the test scripts (the root directory in our case). The location must be changed if the current directory is not the same as the script root directory.

## Test Coverage

- To check the test coverage :
pip install pytest-cov
py.test --cov=. . --cov-report html

# Reference
Find more details about the requirements here :
[https://confluence.rdpnts.com/display/IKB/Python+developer+technical+task]

# Remark

In this implementation we considered returning only the links related to the search terms. But we can easily extend it to return also the owner of the projects and the stats of the use of the programming language.



