from GroceryScraper.groceryscraper.processing_prices.wegmans_process_prices import WegmansProcessPrices

def test_find_units():
    process_price = WegmansProcessPrices()
    price = "1 gal ($6.49/gal)"
    units = process_price.find_units(price)
    assert units[0] == "gal"
    assert not units[1]

    price = "59 fl oz ($0.08/fl oz)"
    units = process_price.find_units(price)
    assert units[0] == 'fl'
    assert not units[1]

    price = "24 oz ($0.06/oz)"
    units = process_price.find_units(price)
    assert units[0] == 'oz'
    assert not units[1]

    # Need to add
    price = "32 oz bag ($0.19/oz bag)"
    units = process_price.find_units(price)
    assert units[0] == 'oz'
    assert not units[1]

    price = "1 ct ($0.49/lb)"
    units = process_price.find_units(price)
    assert units[0] == 'ct'
    assert not units[1]

    price = "2 lb Bag ($2.25/lb bag)"
    units = process_price.find_units(price)
    assert units[0] == 'lb'
    assert not units[1]

    price = "1 qt ($1.32/qt)"
    units = process_price.find_units(price)
    assert units[0] == 'qt'
    assert not units[1]

    price = "168 ct ($0.15/ct)"
    units = process_price.find_units(price)
    assert units[0] == 'ct'
    assert not units[1]

    price = "10 lb ($1.70/lb)"
    units = process_price.find_units(price)
    assert units[0] == 'lb'
    assert not units[1]

    price = "$13.99/lb"
    units = process_price.find_units(price)
    assert units[0] == 'lb'
    assert not units[1]

    price = "635.8 sq ft ($0.03/sq ft)"
    units = process_price.find_units(price)
    assert units[0] == 'sq ft'
    assert not units[1]

    price = "12 x 50.7 fl oz ($1.25/ea)"
    units = process_price.find_units(price)
    assert units[0] == 'fl'
    assert units[1] == 'ea'

    price = "4 x 5.3 oz ($1.17/ea)"
    units = process_price.find_units(price)
    assert units[0] == 'oz'
    assert units[1] == 'ea'

    price = "4 each ($1.17/each)"
    units = process_price.find_units(price)
    assert units[0] == 'each'
    assert not units[1]

    price = "32 x 8 lb ($0.92/ea)"
    units = process_price.find_units(price)
    assert units[0] == 'lb'
    assert units[1] == 'ea'


def test_convert_lb_ea():
    process_price = WegmansProcessPrices()
    price = [16, 5.99]
    units = ["lb", "ea"]
    convert = 16 * 16
    expected = round((5.99 / convert), 2)
    assert expected == process_price.convert(price, units)


def test_convert_lb():
    process_price = WegmansProcessPrices()
    price = [10, 1.70]
    units = ["lb", None]
    expected = round((1.70 / 16), 2)
    assert expected == process_price.convert(price, units)

def test_convert_gal():
    process_price = WegmansProcessPrices()
    price = [1, 5.99]
    units = ["gal", None]
    expected = round((5.99/128), 2)
    assert expected == process_price.convert(price, units)

