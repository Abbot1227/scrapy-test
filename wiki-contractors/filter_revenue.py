import json
import re


# TODO add real time conversion function
conversion_rates = {

}


def convert_to_usd(amount, currency):
    if currency in conversion_rates:
        return amount * conversion_rates[currency]
    return amount


def filter_revenue(data):
    for entry in data:
        filtered_revenue = []
        year = ""
        for item in entry.get("revenue", []):
            if "US$" or "USD" or "$" in item:
                if "million" in item or "billion" in item:
                    filtered_revenue.append(item)
            elif re.search(r'\(\d{4}\)', item):
                year_match = re.search(r'\((\d{4})\)', item)
                if year_match:
                    year = year_match.group(1)
            else:
                # extract amount and currency
                match = re.search(r'(\d+(\.\d+)?)\s*(\w+)', item)
                if match:
                    amount = float(match.group(1))
                    currency = match.group(3)
                    if currency in conversion_rates:
                        amount_in_usd = convert_to_usd(amount, currency)
                        filtered_revenue.append(f"US${amount_in_usd:.2f} million")
                    else:
                        filtered_revenue.append("amount not in dollars")
                else:
                    filtered_revenue.append("amount not in dollars")

        entry["revenue"] = filtered_revenue
        if year:
            entry["year"] = year
        else:
            entry.pop("year", None)
    return data


def main():
    with open('/urls/urls/16august_merged_contractors.json', 'r') as file:
        data = json.load(file)

    # Filter revenue
    filtered_data = filter_revenue(data)

    with open('merged_contractors_result_filtered_price.json', 'w') as file:
        json.dump(filtered_data, file, indent=2)


if __name__ == "__main__":
    main()
