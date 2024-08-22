# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import json
import re
import requests
import wikipediaapi as wiki
from urllib.parse import urlparse
from itemadapter import ItemAdapter

class UrlsPipeline:
    unwanted_substrings = ['CORP.', 'CO.', '.INT', 'LLC', 'LTD', 'INC', 'GMBH', 'SA', 'AG', 'BV', 'NV', 'PLC', 'PTE', 'SDN',
                           'BHD', 'PTY', 'LIMITED', 'S.A.', '.LTD', 'CO.,', 'CO.,LTD', 'CO.,LTD.', 'CO., LTD', 'INC.',
                           '|']
    language_codes = {'Austria': 'de', 'Greece': 'el', 'Germany': 'de', 'France': 'fr', 'Italy': 'it', 'Spain': 'es',
                      'Denmark': 'da', 'India': 'hi', 'Sweden': 'sv', 'Saudi Arabia': 'ar', 'United Arab Emirates': 'ar',
                      'Belgium': 'nl', 'Netherlands': 'nl', 'Norway': 'no', 'Finland': 'fi', 'Portugal': 'pt',
                      'Poland': 'pl', 'Switzerland': 'de', 'Turkey': 'tr', 'Russia': 'ru', 'Ukraine': 'uk',
                      'United Kingdom': 'en', 'Chine': 'zh', 'Japan': 'ja', 'South Korea': 'ko', 'Malaysia': 'ms',
                      'South Africa': 'af', 'Luxembourg': 'lb', 'Singapore': 'ms', 'Romania': 'ro', 'Hungary': 'hu',
                      'Serbia': 'sr', 'Croatia': 'hr', 'Slovenia': 'sl', 'Bulgaria': 'bg', 'Czech Republic': 'cs',
                      'Taiwan': 'zh', 'Vietnam': 'vi', 'Thailand': 'th', 'Indonesia': 'id', 'Philippines': 'tl',
                      'Qatar': 'ar', 'Kuwait': 'ar', 'Lebanon': 'ar', 'Chile': 'es', 'Israel': 'he', 'Egypt': 'ar'}
    country_categories = {'ko': '대한민국의 건설 기업'} # TODO finish

    def clean_company_name(self, name: str) -> str:
        for substring in self.unwanted_substrings:
            name = re.sub(r'\b' + re.escape(substring) + r'\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+', ' ', name).strip()
        name = name.replace(' ', '_')
        return name

    def search_by_url(self, website: str, country: str, wiki_wiki: wiki.Wikipedia) -> (bool, str):
        if website == '':
            return False, ''
        language_code = 'en'
        parsed_url = urlparse(website)

        domain_parts = parsed_url.netloc.split('.')
        if domain_parts[0] == 'www':
            domain_parts = domain_parts[1:]

        search_query = parsed_url.netloc
        number_of_results = 4
        headers = {
            'User-Agent': 'myTest (tengri123ax@gmail.com)'
        }
        base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
        endpoint = '/search/page'
        url = base_url + language_code + endpoint
        parameters = {'q': search_query, 'limit': number_of_results}

        response = requests.get(url, headers=headers, params=parameters)
        response = json.loads(response.text)

        if 'pages' in response:
            for page in response['pages']:
                name = page['key']
                exist, url = self.search_wikipedia(name, wiki_wiki)
                if exist:
                    return True, url
        elif country in self.language_codes:
            language_code = self.language_codes[country]
            wiki_wiki.language = language_code
            url = base_url + language_code + endpoint
            parameters = {'q': search_query, 'limit': number_of_results}

            response = requests.get(url, headers=headers, params=parameters)
            response = json.loads(response.text)

            if 'pages' in response:
                for page in response['pages']:
                    name = page['key']
                    exist, url = self.search_wikipedia_with_country(name, wiki_wiki, language_code)
                    if exist:
                        wiki_wiki.language = 'en'
                        return True, url
            else:
                wiki_wiki.language = 'en'
        return False, ''

    def search_by_name(self, name: str, country: str, wiki_wiki: wiki.Wikipedia) -> (bool, str):
        language_code = 'en'
        search_query = name
        number_of_results = 4
        headers = {
            'User-Agent': 'myTest (tengri123ax@gmail.com)'
        }
        base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
        endpoint = '/search/page'
        url = base_url + language_code + endpoint
        parameters = {'q': search_query, 'limit': number_of_results}

        response = requests.get(url, headers=headers, params=parameters)
        response = json.loads(response.text)

        if 'pages' in response:
            for page in response['pages']:
                name = page['key']
                exist, url = self.search_wikipedia(name, wiki_wiki)
                if exist:
                    return True, url
        if country in self.language_codes:
            language_code = self.language_codes[country]
            wiki_wiki.language = language_code
            url = base_url + language_code + endpoint
            parameters = {'q': search_query, 'limit': number_of_results}

            response = requests.get(url, headers=headers, params=parameters)
            response = json.loads(response.text)

            if 'pages' in response:
                for page in response['pages']:
                    name = page['key']
                    exist, url = self.search_wikipedia_with_country(name, wiki_wiki, language_code)
                    if exist:
                        wiki_wiki.language = 'en'
                        return True, url
            else:
                wiki_wiki.language = 'en'
        return False, ''

    def search_wikipedia(self, name, wiki_wiki: wiki.Wikipedia) -> (bool, str):
        page = wiki_wiki.page(name)
        exists = page.exists()

        country_category = 'Construction and civil engineering companies'
        in_category = any(country_category in category for category in page.categories.keys())
        if exists and in_category:
            return True, page.fullurl
        else:
            return False, ''

    def search_wikipedia_with_country(self, name, wiki_wiki: wiki.Wikipedia, language_code) -> (bool, str):
        if language_code != 'ko':
            return False, ''
        page = wiki_wiki.page(name)
        exists = page.exists()

        country_category = self.country_categories[language_code]
        in_category = any(country_category in category for category in page.categories.keys())
        if exists and in_category:
            return True, page.fullurl
        else:
            return False, ''

    def process_item(self, item, spider):
        contractor = item['contractor']
        wiki_wiki = wiki.Wikipedia('test (tengr123ax@gmail.com', 'en')

        website, country = contractor["website"], contractor["country"]
        step3, url = self.search_by_url(website, country, wiki_wiki)
        if step3:
            contractor['url'] = url
            return contractor

        cleaned_name = self.clean_company_name(contractor["company name"])
        step1, url = self.search_by_name(cleaned_name, contractor["country"], wiki_wiki)
        if step1:
            contractor['url'] = url
            return contractor

        title_case_name = cleaned_name.title()
        step2, url = self.search_by_name(title_case_name, contractor["country"], wiki_wiki)
        if step2:
            contractor['url'] = url
            return contractor

        return contractor
