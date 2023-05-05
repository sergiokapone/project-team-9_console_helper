from collections import namedtuple, UserList
import requests
from prettytable import PrettyTable


Currency = namedtuple("Currency", ["name", "rate", "cc"])


class CurrencyList(UserList):
    URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json"

    def __init__(self):
        super().__init__()
        self.refresh()

    def refresh(self):
        response = requests.get(self.URL)
        data = response.json()
        for item in data:
            if item.get("cc") in ("USD", "EUR", "XAU", "XAG", "XPT", "XPD"):
                currency = Currency(item.get("txt"), item.get("rate"), item.get("cc"))
                self.data.append(currency)

    def get_currency_by_cc(self, cc: str) -> Currency:
        for currency in self.data:
            if currency.cc == cc:
                return currency

    def get_currency_rates(self):
        return self.data


if __name__ == "__main__":

    def get_currency_table(currency_list: CurrencyList):
        table = PrettyTable()
        table.max_width["Currency"] = 30
        table.max_width["Short Name"] = 15
        table.max_width["Rate"] = 10
        table.align["Short Name"] = "c"
        table.align["Rate"] = "c"
        table.field_names = ["Currency", "Short Name", "Rate"]
        for currency in currency_list.get_currency_rates():
            table.add_row([currency.name, currency.cc, currency.rate])
        return table

    cur = CurrencyList()
    get_currency_table(cur)
