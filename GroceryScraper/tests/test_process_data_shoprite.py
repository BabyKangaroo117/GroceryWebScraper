from GroceryScraper.groceryscraper.processing_prices.shoprite_process_prices import ShopriteProcessPrices

def test_find_units():
    process_price = ShopriteProcessPrices()
    price_1 = "$3.49/lb"
    units = process_price.find_units(price_1)
    assert units == "lb"

    price_2 = "$0.20/oz"
    units = process_price.find_units(price_2)
    assert units == 'oz'


def test_process_price():
    process_price = ShopriteProcessPrices()
    price_1 = "$3.49/lb"
    processed_price = process_price.process_individual_price(price_1)
    assert float(processed_price) == 3.49

def test_convert_lb():
    process_price = ShopriteProcessPrices()
    price = "3.49"
    units = "lb"
    expected = round((float(price)/16), 2)
    assert expected == process_price.convert(price, units)

def test_convert_grams():
    process_price = ShopriteProcessPrices()
    price = "0.02"
    units = "g"
    expected = round((float(price)/0.03527396), 2)
    assert expected == process_price.convert(price, units)



