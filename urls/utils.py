import json
import csv
import re
import pandas as pd
from collections import defaultdict


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Converting json to csv so that it can be opened on excel
def write_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(data[0].keys())
        # Write the data
        for row in data:
            writer.writerow(row.values())


def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def combine_and_convert():
    # Read JSON data from files
    json_data1 = read_json('/home/tengr/PycharmProjects/scrapy-test/urls/indonesia/todayglobal_energy_time_2024-09-06T06-01-09.997856+00-00.json')
    json_data2 = read_json('/home/tengr/PycharmProjects/scrapy-test/urls/indonesia/todaywiki_time_2024-09-06T06-02-30.210160+00-00.json')

    # Combine data if necessary
    combined_data = json_data1 + json_data2

    # Write combined data to CSV
    write_csv(combined_data, 'combined_data.csv')


def remove_duplicates():
    json_data1 = read_json('/home/tengr/PycharmProjects/scrapy-test/urls/indonesia/todayglobal_energy_time_2024-09-06T06-01-09.997856+00-00.json')
    json_data2 = read_json('/home/tengr/PycharmProjects/scrapy-test/urls/indonesia/todaywiki_time_2024-09-06T06-02-30.210160+00-00.json')

    processed_data = process_data(json_data1, json_data2)
    save_json(processed_data, 'processed_data.json')


def normalize_name(name):
    # Remove unnecessary labels from the name
    name = re.sub(r'\b(Indonesia|power|plant|station)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def process_data(first_data, second_data):
    combined_data = defaultdict(lambda: {
        'capacity': 0, 'count': 0, 'source': '', 'location': '', 'sublocation': '',
        'plant_type': '', 'status': '', 'secondary_fuel': '', 'primary_fuel': '', 'full_name': ''
    })

    # Process global data first (priority)
    for entry in second_data:
        if 'name' in entry:
            normalized_name = normalize_name(entry['name'])
            capacity = float(entry['capacity'].strip())
            combined_data[normalized_name]['capacity'] += capacity
            combined_data[normalized_name]['count'] += 1
            combined_data[normalized_name]['source'] = entry.get('source', combined_data[normalized_name]['source'])
            combined_data[normalized_name]['location'] = entry.get('location', combined_data[normalized_name]['location'])
            combined_data[normalized_name]['sublocation'] = entry.get('sublocation', combined_data[normalized_name]['sublocation'])
            combined_data[normalized_name]['plant_type'] = entry.get('plant_type', combined_data[normalized_name]['plant_type'])
            combined_data[normalized_name]['status'] = entry.get('status', combined_data[normalized_name]['status'])
            combined_data[normalized_name]['secondary_fuel'] = entry.get('secondary_fuel', combined_data[normalized_name]['secondary_fuel'])
            combined_data[normalized_name]['primary_fuel'] = entry.get('primary_fuel', combined_data[normalized_name]['primary_fuel'])
            combined_data[normalized_name]['full_name'] = entry['name']

    # Process wiki data
    for entry in first_data:
        if 'name' in entry:
            normalized_name = normalize_name(entry['name'])
            capacity = float(entry['capacity'].strip())
            combined_data[normalized_name]['capacity'] += capacity
            combined_data[normalized_name]['count'] += 1
            combined_data[normalized_name]['source'] = entry.get('source', combined_data[normalized_name]['source'])
            combined_data[normalized_name]['location'] = entry.get('location', combined_data[normalized_name]['location'])
            combined_data[normalized_name]['sublocation'] = entry.get('sublocation', combined_data[normalized_name]['sublocation'])
            combined_data[normalized_name]['plant_type'] = entry.get('plant_type', combined_data[normalized_name]['plant_type'])
            combined_data[normalized_name]['status'] = entry.get('status', combined_data[normalized_name]['status'])
            combined_data[normalized_name]['secondary_fuel'] = entry.get('secondary_fuel', combined_data[normalized_name]['secondary_fuel'])
            combined_data[normalized_name]['primary_fuel'] = entry.get('primary_fuel', combined_data[normalized_name]['primary_fuel'])
            combined_data[normalized_name]['full_name'] = entry['name']

    # Divide capacities by the number of duplicates
    result = []
    for name, data in combined_data.items():
        data['capacity'] /= data['count']
        result.append({
            'name': name,
            'capacity': data['capacity'],
            'source': data['source'],
            'location': data['location'],
            'sublocation': data['sublocation'],
            'plant_type': data['plant_type'],
            'status': data['status'],
            'secondary_fuel': data['secondary_fuel'],
            'primary_fuel': data['primary_fuel'],
            'full_name': data['full_name'],
            'count': data['count']
        })

    return result


def find_powerplant_capacity(text):
    # Regexp to match the number followed by MW
    pattern = r'(\d+)\s*(?:-megawatts|MW)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def save_structured_csv(data, file: str):
    # Normalizing data so it can nbe used in pandas dataframe
    normalized_data = []
    for item in data:
        base_info = {k: v for k, v in item.items() if k != 'units'}
        units = item.get('units', {})
        if 'Unit name' in units:
            for i in range(len(units['Unit name'])):
                unit_info = {k: v[i] for k, v in units.items()}
            combined_info = {**base_info, **unit_info}
            normalized_data.append(combined_info)
        else:
            print("Key 'Unit name' not found in units dictionary")

    df = pd.DataFrame(normalized_data)
    df.to_csv(file, index=False)

if __name__ == '__main__':
    # remove_duplicates()
    with open('/home/tengr/PycharmProjects/scrapy-test/urls/indonesia/todaygemwiki_time_2024-09-09T06-06-29.414264+00-00.json', 'r') as file:
        data = json.load(file)
    save_structured_csv(data, 'gemwiki.csv')
