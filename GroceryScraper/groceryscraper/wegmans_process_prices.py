import re


# Edge cases
# 32 x 1 lb ($0.92/ea)
# 2 lb ($2.40/lb)
# 12 x 50.7 fl oz ($1.25/ea)


class WegmansProcessPrices:
    def __init__(self):
        pass

    def process_price_converted(self, raw_unit_price):
        units = self.find_units(raw_unit_price)
        processed = self.process(raw_unit_price)
        unit_price_converted = self.convert(processed, units)
        return unit_price_converted

    def find_units(self, raw_unit_price):
        units = re.search(r'\bgal\b|\boz\b|\bfl\b|\bqt\b|\bct\b|\blb\b|\beach\b|\bea\b|\bsq ft\b|\bpint\b|\bl\b'
                          r'|\bbunch\b',raw_unit_price)
        each = re.search(r'\bea\b', raw_unit_price)
        if each:
            unit_list = [units.group(), each.group()]
        else:
            unit_list = [units.group(), None]
        return unit_list

    def process(self, raw_unit_price):
        processed = re.sub(r'|bunch|container|pint|gal|fl|oz|qt|ct|lb|each|ea|sq|bag|ft|l|L|/|\(|\)|\$|', "", raw_unit_price)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        return split_processed

    def convert(self, price: list, units: list):
        """Convert units to oz if solid or fl oz if liquid. Products that are ct or sq ft, stay the same
        Three formats: [price_per_unit], [amount, unit_price], [amount, size, price_per_unit]"""
        if units[1]:
            num_units = float(price[-2])
            price_per_unit = float(price[-1])
            convert_units = round(num_units * self.converstion_table(units[0]), 2)
            unit_price_converted = round((price_per_unit / convert_units), 2)
            return unit_price_converted
        else:
            price_per_unit = float(price[-1])
            unit_price_converted = round(price_per_unit / self.converstion_table(units[0]), 2)
            return unit_price_converted

    def converstion_table(self, unit: str):
        """Convert unit price solids to oz and liquids to fl oz"""
        unit_conversions = {
            "fl": 1,
            "oz": 1,
            "lb": 16,
            "l": 33.814,
            "gal": 128,
            "qt": 32,
            "pint": 16,
            "sq ft": 1,
            "ct": 1,
            "each": 1,
            "ea": 1,
            "bunch": 1
        }
        return unit_conversions[unit]

    def convert_unit_type(self, unit):
        if unit in ["fl", "gal", "l", "qt"]:
            return "fl oz"
        elif unit in ["oz", "lb", "kg", "pint"]:
            return "oz"
        else:
            return unit



