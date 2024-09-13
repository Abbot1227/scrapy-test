from urllib.parse import urlparse
import json
from googlesearch import search


projects = ['Wolyla Copper Gold Project',
            'Wongogiri Copper Gold Project',
            'Trenggalek - Gold',
            'Idenburg  - Gold',
            'Grasberg Block Cave Mine - Gold',
            'Deep Mill Level Zone Mine - Gold',
            'Batu Hijau Mine - Gold',
            'Martabe Project - Gold',
            'Toka Tindung Gold Project',
            'Sangatta Mine - Coal',
            'FTB Project - Coal',
            'Tutupan Mine - Coal',
            'Borneo Indobara Mine - Coal',
            'Pasir Mine - Coal',
            'Weda Bay Project - Nickel',
            'PT Halmahera Persada Lygend Project - Nickel',
            'Sorowako Mine - Nickel',
            'PT Huayue Nickel Cobalt Project - Nickel',
            'Pakal Island Mine - Nickel',
            'Grasberg Block Cave Mine - Copper',
            'Deep Mill Level Zone Mine - Copper',
            'Batu Hijau Mine - Copper',
            'Big Gossan Underground Mine - Copper',
            'Wetar Copper Project',
            'Pani Gold Project',
            'Tujuh Bukit Copper Project',
            'Awak Mas Gold Project']
urls = []

def fetch_top_search_results(query, num_results):
    search_results = search(query, num_results=num_results)
    return search_results

if __name__ == "__main__":
    for project in projects:
        search_query = project + ' mining technology'
        top_results = fetch_top_search_results(search_query, num_results=6)

        for idx, result in enumerate(top_results, 1):
            #if result[0:42] == 'https://www.mining-technology.com/projects':
            #    print(f'Project {project} with url {result}')
            #    urls.append(result)
            #    break
            url = urlparse(result)
            if url.netloc == 'www.mining-technology.com':
                urls.append(result)
                break

    # save urls to json file
    with open('../mining_urls_new.json', 'w') as f:
        json.dump(urls, f)
    print('finished')