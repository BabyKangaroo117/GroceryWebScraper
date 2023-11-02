from GroceryScraper.groceryscraper.wegmans_process_prices import WegmansProcessPrices

def test_find_units():
    process_price = WegmansProcessPrices()
    price_1 = "1 gal ($5.99/gal)"
    units = process_price.find_units(price_1)
    assert units[0] == "gal"
    assert not units[1]

    price_2 = "12 x 50.7 fl oz ($1.25/ea)"
    units = process_price.find_units(price_2)
    assert units[0] == 'fl'
    assert units[1] == 'ea'


def test_convert():
    process_price = WegmansProcessPrices()
    price = [16, 5.99]
    units = ["lb", "ea"]
    convert = 16 * 16
    expected = round((5.99 / convert), 2)
    assert expected == process_price.convert(price, units)


