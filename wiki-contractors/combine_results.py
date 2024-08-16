import json
import time


def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)


def merge_json_files(file_paths):
    merged_data = []
    seen_numbers = set()

    for file_path in file_paths:
        data = read_json(file_path)
        for company in data:
            if company['No.'] not in seen_numbers:
                merged_data.append(company)
                seen_numbers.add(company['No.'])
            # TODO think how to optimize
            if company['No.'] in seen_numbers and len(company['revenue']) < 0:
                merged_data.append(company)
                seen_numbers.add(company['No.'])
    return merged_data


def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def main():
    start_time = time.time()
    input_files = ['todaycontractors.json',
                   'category)contractors.json']
    output_file = '16august_merged_contractors.json'

    merged_data = merge_json_files(input_files)
    write_json(output_file, merged_data)
    print(f"Merged data written to {output_file}")

    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
