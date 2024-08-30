import json
import re
import time
import requests

import wikipediaapi as wiki
from urllib.parse import urlparse

# Prefixes I do not need
unwanted_substrings = ['CORP.', 'CO.', '.INT', 'LLC', 'LTD', 'INC', 'GMBH', 'SA', 'AG', 'BV', 'NV', 'PLC', 'PTE', 'SDN',
                       'BHD', 'PTY', 'LIMITED', 'S.A.', '.LTD', 'CO.,', 'CO.,LTD', 'CO.,LTD.', 'CO., LTD', 'INC.',
                       '|', 'Public', 'Joint', 'Company', 'Stock']

language_codes = {'Austria': 'de', 'Greece': 'el', 'Germany': 'de', 'France': 'fr', 'Italy': 'it', 'Spain': 'es',
                  'Denmark': 'da', 'India': 'hi', 'Sweden': 'sv', 'Saudi Arabia': 'ar', 'United Arab Emirates': 'ar',
                  'Belgium': 'nl', 'Netherlands': 'nl', 'Norway': 'no', 'Finland': 'fi', 'Portugal': 'pt',
                  'Poland': 'pl', 'Switzerland': 'de', 'Turkey': 'tr', 'Russia': 'ru', 'Ukraine': 'uk',
                  'United Kingdom': 'en', 'Chine': 'zh', 'Japan': 'ja', 'South Korea': 'ko', 'Malaysia': 'ms',
                  'South Africa': 'af', 'Luxembourg': 'lb', 'Singapore': 'ms', 'Romania': 'ro', 'Hungary': 'hu',
                  'Serbia': 'sr', 'Croatia': 'hr', 'Slovenia': 'sl', 'Bulgaria': 'bg', 'Czech Republic': 'cs',
                  'Taiwan': 'zh', 'Vietnam': 'vi', 'Thailand': 'th', 'Indonesia': 'id', 'Philippines': 'tl',
                  'Qatar': 'ar', 'Kuwait': 'ar', 'Lebanon': 'ar', 'Chile': 'es', 'Israel': 'he', 'Egypt': 'ar-eg'}

country_categories = {'ko': '대한민국의', 'de': 'Bauunternehmen',
                      'da': 'Bygge-, konstruktions- og anlægsvirksomheder i Danmark', 'ar': 'شركات بناء في مصر',
                      'es': 'Constructoras de España', 'fr': 'Entreprise de la construction ayant son siège en France',
                      'zh': '中國建築公司', 'ja': '日本の建設会社', 'ru': 'Строительные компании России',
                      'ms': 'Companii de construcții din România'}


def clean_company_name(name: str) -> str:
    for substring in unwanted_substrings:
        name = re.sub(r'\b' + re.escape(substring) + r'\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()
    name = name.replace(' ', '_')
    return name


def search_by_url(website: str, country: str, wiki_wiki: wiki.Wikipedia) -> (bool, str):
    if website == '':
        return False, ''
    language_code = 'en'
    parsed_url = urlparse(website)

    domain_parts = parsed_url.netloc.split('.')
    # remove www
    if domain_parts[0] == 'www':
        domain_parts = domain_parts[1:]

    # remove any subdomains
    if len(domain_parts) > 2:
        main_domain = '.'.join(domain_parts[-2:])
    else:
        main_domain = parsed_url.netloc

    # prepare request
    search_query = main_domain
    number_of_results = 4   # company page if usually in first 2 results
    headers = {
        'User-Agent': 'mynews (tengri125ax@gmail.com)'
    }
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}

    #response = requests.get(url, headers=headers, params=parameters)
    #response = json.loads(response.text)

    # if 'pages' in response:
    #     for page in response['pages']:
    #         name = page['key']
    #         exist, url = search_wikipedia(name, wiki_wiki)
    #         if exist:
    #             return True, url
    # # searching page in other language
    # el
    if country in language_codes:
        language_code = 'ms'#language_codes[country]
        wiki_wiki.language = language_code
        # prepare request
        url = base_url + language_code + endpoint
        parameters = {'q': search_query, 'limit': number_of_results}

        response = requests.get(url, headers=headers, params=parameters)

        # TODO temporary solution for rate limiting
        while response.status_code == 429:
            time.sleep(10)
            response = requests.get(url, headers=headers, params=parameters)

        response = json.loads(response.text)


        if 'pages' in response:
            for page in response['pages']:
                name = page['key']
                print("Found page:", name)
                exist, url = search_wikipedia_with_country(name, wiki_wiki, language_code)
                if exist:
                    wiki_wiki.language = 'en'
                    return True, url
        else:
            wiki_wiki.language = 'en'
    return False, ''


def search_by_name(name: str, country: str, wiki_wiki: wiki.Wikipedia) -> (bool, str):
    language_code = 'en'
    search_query = name
    number_of_results = 4
    headers = {
        'User-Agent': 'mywiki (tengri123ax@gmail.com)'
    }
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}

    #response = requests.get(url, headers=headers, params=parameters)
    # TODO temporary solution for rate limiting
    #while response.status_code == 429:
     #   time.sleep(10)
     #   response = requests.get(url, headers=headers, params=parameters)
    #response = json.loads(response.text)

    # if 'pages' in response:
    #     for page in response['pages']:
    #         name = page['key']
    #         exist, url = search_wikipedia(name, wiki_wiki)
    #         if exist:
    #             return True, url
    if country in language_codes:
        language_code = 'ms'#language_codes[country]
        wiki_wiki.language = language_code
        # prepare request
        url = base_url + language_code + endpoint
        parameters = {'q': search_query, 'limit': number_of_results}

        response = requests.get(url, headers=headers, params=parameters)
        response = json.loads(response.text)

        if 'pages' in response:
            for page in response['pages']:
                name = page['key']
                print("Found page:", name)
                exist, url = search_wikipedia_with_country(name, wiki_wiki, language_code)
                if exist:
                    wiki_wiki.language = 'en'
                    return True, url
        else:
            wiki_wiki.language = 'en'
        wiki_wiki.language = 'en'
    return False, ''


def search_wikipedia(name, wiki_wiki: wiki.Wikipedia) -> (bool, str):
    page = wiki_wiki.page(name)
    exists = page.exists()

    # check if page.categories has some substring in one string in it
    country_category = 'Construction and civil engineering companies'
    in_category = any(country_category in category for category in page.categories.keys())
    if exists and in_category:
        return True, page.fullurl
    else:
        return False, ''


def search_wikipedia_with_country(name, wiki_wiki: wiki.Wikipedia, language_code) -> (bool, str):
    if language_code != 'ms':
        return False, ''
    page = wiki_wiki.page(name)
    exists = page.exists()

    # check if page.categories has some substring in one string in it
    country_category = country_categories[language_code]
    in_category = any(country_category in category for category in page.categories.keys())
    if exists and in_category:
        return True, page.fullurl
    else:
        return False, ''


def start_search(input_file: str, output_file: str, wiki_wiki: wiki.Wikipedia):
    with open(input_file, 'r') as f:
        companies = json.load(f)

    results = []
    process_search(companies, results, wiki_wiki, output_file)


def process_search(companies, results, wiki_wiki, output_file):
    for company in companies:
        original_name = company["company name"]

        # TODO create separate function for this
        if company['country'] != 'Romania':
            continue

        print("Processing: ", company["No."], original_name)

        website, country = company["website"], company["country"]
        step1, url = search_by_url(website, country, wiki_wiki)
        if step1:
            add_to_results(company, "Step 1", url, results, output_file)
            continue

        cleaned_name = clean_company_name(original_name)
        step2, url = search_by_name(cleaned_name, company["country"], wiki_wiki)
        if step2:
            add_to_results(company, "Step 2", url, results, output_file)
            continue

        title_case_name = cleaned_name.title()
        step3, url = search_by_name(title_case_name, company["country"], wiki_wiki)
        if step3:
            add_to_results(company, "Step 3", url, results, output_file)
            continue


i = 0


def add_to_results(company, step: str, url: str, results, output_file):
    global i
    i += 1
    result = {
        "No.": company["No."],
        "company name": company["company name"],
        "website": company["website"],
        "url": url,
        "country": company["country"],
        "continent": company["continent"],
        "source": "Wikipedia"
    }
    results.append(result)
    print(f'{company["No."]}. {step}; {company["company name"]} exists on Wikipedia {url}. Total processed: {i}')

    # Add result as object to array in json file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)


def main():
    start = time.time()

    wiki_wiki = wiki.Wikipedia('test (tengr123ax@gmail.com', 'en')
    start_search('by_country.json', '../urls/results_by_romania.json', wiki_wiki)

    end = time.time()
    print("Time elapsed (seconds):", end - start)


if __name__ == '__main__':
    main()
