import json
import os.path

import currencyapicom
from dotenv import load_dotenv

load_dotenv()

# CurrencyConverter is a class that provides a way to convert
# between different currencies using the currencyapi.com API
class CurrencyConverter:
    def __init__(self, path: str):
        self.path = path
        if self.exists():
            with open(self.path, 'r') as f:
                self.rates = json.load(f)
        else:
            self.update_rates()

    def exists(self):
        return os.path.exists(self.path)

    # get_rate returns the exchange rate for the
    # given currency with dollar as base currency
    def get_rate(self, value,  currency: str):
        rate = self.rates[currency]
        return value / rate

    # update_rates retrieves the latest exchange rates
    # from the API and stores them in a file if it does not exist
    def update_rates(self):
        # read value from environment variable
        api_key = os.getenv('API_KEY')
        if not api_key:
            print('API_KEY not found')
            return

        client = currencyapicom.Client(api_key)
        result = client.latest()
        for rate in result['data']:
            self.rates[rate['code']] = float(rate['value'])

        with open(self.path, 'w') as f:
            json.dump(self.rates, f)
