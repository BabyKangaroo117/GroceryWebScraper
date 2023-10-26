import re


# Edge cases
# 32 x 1 lb ($0.92/ea)
# 2 lb ($2.40/lb)
# 12 x 50.7 fl oz ($1.25/ea)


class ProcessPrices:
    def __init__(self):
        pass

    def process_price(self, raw_unit_price):
        units = self.find_units(raw_unit_price)
        processed = self.process(raw_unit_price)
        unit_price_converted = self.convert(processed, units)
        return unit_price_converted

    def find_units(self, raw_unit_price):
        units = re.search(r'gal|oz|fl|qt|ct|lb|sq', raw_unit_price)
        type = re.search(r'ea', raw_unit_price)
        if type:
            unit_list = [units.group(), type.group()]
        else:
            unit_list = [units.group(), None]
        return unit_list

    def process(self, raw_unit_price):
        processed = re.sub(r'gal|fl|oz|ea|qt|ct|lb|(|)|$|', "", raw_unit_price)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        return split_processed

    def convert(self, price: list, units: list):
        if units[1]:
            num_units = price[-2]
            price_per_unit = price[-1]
            convert_units = round(num_units * self.converstion_table(units[0]), 2)
            unit_price_converted = round((price_per_unit / convert_units), 2)
            return unit_price_converted
        else:
            price_per_unit = price[-1]
            unit_price_converted = round(price_per_unit / self.converstion_table(units[0]), 2)
            return unit_price_converted

    def converstion_table(self, unit: str):
        """Convert unit price solids to oz and liquids to fl oz"""
        unit_conversions = {
            "fl": 1,
            "oz": 1,
            "lb": 16,
            "kg": 35.274,
            "g": 0.035,
            "Tablespoon": 0.5,
            "Teaspoon": 0.17,
            "L": 33.814,
            "Milliliters": 0.034,
            "gal": 128,
            "qt": 32,
            "Pint": 16,
            "Cup": 8,
            "sq": 1,
            "ct": 1
        }
        return unit_conversions[unit]



