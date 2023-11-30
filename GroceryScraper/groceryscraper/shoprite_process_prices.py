import re


# Edge cases
# 32 x 1 lb ($0.92/ea)
# 2 lb ($2.40/lb)
# 12 x 50.7 fl oz ($1.25/ea)


class ShopriteProcessPrices:
    def __init__(self):
        pass

    def process_individual_price(self, raw_price):
        processed = re.sub(r'gal|fl|oz|each|qt|ct|lb|\(|\)|\$|/|ea| |avg|pint|', "", raw_price)
        return processed


    def process_unit_price(self, raw_unit_price):
        units = self.find_units(raw_unit_price)
        print(units)
        processed = self.process(raw_unit_price)
        print(processed)
        unit_price_converted = self.convert(processed, units)
        return unit_price_converted

    def find_units(self, raw_unit_price):
        units = re.search(r'\bgal\b|\bfl oz\b|\boz\b|\bqt\b|\bct\b|\blb\b|lb|\beach\b|\bea\b|\bsq ft\b|\bpint\b'
                          r'|\bl\b|\bbunch\b|\bpt\b|\bg\b',
                          raw_unit_price)
        try:
            unit = units.group()
        except AttributeError:
            unit = "Not found"
        return unit

    def process(self, raw_unit_price):
        processed = re.sub(r'gal|fl|oz|each|qt|ct|lb|\(|\)|\$|/| |ea|sq|pint|pt|l|bunch|g|', "", raw_unit_price)
        return processed

    def convert(self, price, units):
        try:
            unit_price_converted = round(float(price) / self.converstion_table(units), 2)
        except (KeyError, ValueError):
            unit_price_converted = "Not found"
        return unit_price_converted

    def converstion_table(self, unit: str):
        """Convert unit price solids to oz and liquids to fl oz"""
        unit_conversions = {
            "fl oz": 1,
            "oz": 1,
            "lb": 16,
            "l": 33.814,
            "gal": 128,
            "qt": 32,
            "pt": 16,
            "g": 28.3495,
            "sq ft": 1,
            "ct": 1,
            "each": 1,
            "ea": 1,
            "bunch": 1
        }
        return unit_conversions[unit]

    def convert_unit_type(self, unit):
        if unit in ["fl oz", "gal", "l", "qt"]:
            return "fl oz"
        elif unit in ["oz", "lb", "kg", "pint", "g"]:
            return "oz"
        else:
            return unit



