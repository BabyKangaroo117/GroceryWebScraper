class ProcessPrices:
    def process_gal(self, price: str):
        """String with format '1 gal ($4.36/gal)' """

        processed: str = (price.
                          replace("gal", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "")
                          )

        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        value_to_convert = float(split_processed[1])
        unit_price = self._conv_table_liquids("Gallon", value_to_convert, True)
        return unit_price

    def process_quart(self, price: str):
        """String with format '1 qt ($1.32/qt)' """

        processed: str = (price.
                          replace("qt", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "")
                          )

        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        value_to_convert = float(split_processed[1])
        unit_price = self._conv_table_liquids("Quart", value_to_convert, True)
        return unit_price

    def process_ounces(self, price: str):
        """String with format '32 oz ($0.08/oz)' """
        processed: str = (price.
                          replace("oz", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        unit_price = float(split_processed[1])

        return unit_price

    def process_fl_ounces(self, price: str):
        """String with format '50 fl oz ($0.06/fl oz)' """
        processed: str = (price.
                          replace("fl", "").
                          replace("oz", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        unit_price = float(split_processed[1])

        return unit_price

    def process_fl_oz_ea(self, price):
        """String with format '12 x 12 fl oz ($0.33/ea)' """
        processed: str = (price.
                          replace("fl", "").
                          replace("x", "").
                          replace("oz", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "").
                          replace("ea", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        price_per_unit = float(split_processed[2])
        num_fl_oz_per_unit = float(split_processed[1])
        print(split_processed)
        unit_price = round(float(price_per_unit / num_fl_oz_per_unit), 2)

        return unit_price

    def process_oz_ea(self, price):
        """String with format '6 x 3 oz ($0.45/ea)' """
        processed: str = (price.
                          replace("x", "").
                          replace("oz", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "").
                          replace("ea", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        price_per_unit = float(split_processed[2])
        num_oz_per_unit = float(split_processed[1])
        unit_price = round(float(price_per_unit / num_oz_per_unit), 2)

        return unit_price

    def process_lb_ea(self, price):
        """String with format '32 x 8 lb ($0.92/ea)' """
        processed: str = (price.
                          replace("x", "").
                          replace("lb", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "").
                          replace("ea", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        price_per_unit = float(split_processed[2])
        num_lb = float(split_processed[1])
        converted = self._conv_table_solids("Pound", num_lb, False)
        unit_price = round(float(price_per_unit / converted), 2)

        return unit_price

    def process_lbs(self, price: str):
        """String with format '$13.99/lb' """
        processed = float(price.replace("lb", "").replace("/", "").replace("$", ""))
        converted = self._conv_table_solids("Pound", processed, True)
        return converted

    def process_multi_lbs(self, price: str):
        """String with format of '10 lb ($1.70/lb)' """
        processed: str = (price.
                          replace("lb", "").
                          replace("(", "").
                          replace(")", "").
                          replace("/", "").
                          replace("$", "")
                          )

        # Ex processed format is "16 0.60" which is "(num ounces) (price per ounce)
        split_processed = processed.split(" ")
        # Remove empty strings
        split_processed = [item for item in split_processed if item]
        print(split_processed)
        price_per_unit = float(split_processed[1])
        print(price_per_unit)
        converted = self._conv_table_solids("Pound", price_per_unit, True)
        print(converted)
        return converted


    def process_count(self, price):
        pass

    def _conv_table_solids(self, unit: str, value: int, per_unit: bool):
        """Convert Unit Prices to ounces"""
        unit_conversions = {
            "Pound": 16,
            "Kilogram": 35.274,
            "Gram": 0.035,
            "Tablespoon": 0.5,
            "Teaspoon": 0.17
        }

        if per_unit:
            return round(value / unit_conversions[unit], 2)
        else:
            return round(value * unit_conversions[unit], 2)

    def _conv_table_liquids(self, unit: str, value: int, per_unit: bool):
        """Unit prices to fl oz"""
        unit_conversions = {
            "Liter": 33.814,
            "Milliliters": 0.034,
            "Gallon": 128,
            "Quart": 32,
            "Pint": 16,
            "Cup": 8
        }
        if per_unit:
            return round(value / unit_conversions[unit], 2)
        else:
            return round(value * unit_conversions[unit], 2)

