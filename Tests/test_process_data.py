import os,  sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from webscraper import WebScraper
import process_prices

def test_process_gal():

    process = process_prices.ProcessPrices()
    price = "1 gal ($5.99/gal)"

    expected_output = round((5.99 / 128), 2)  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_gal(price) == expected_output

    # Add more test cases as needed
    price_2 = "3 gal ($5.99/gal)"
    expected_output_2 = round((5.99 / 128), 2)
    assert process.process_gal(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_process_oz():

    process = process_prices.ProcessPrices()
    price = "24 oz ($0.27/oz)"

    expected_output = 0.27  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_ounces(price) == expected_output

    # Add more test cases as needed
    price_2 = "13.5 oz ($0.15/oz)"
    expected_output_2 = 0.15
    assert process.process_ounces(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_process_qt():
    process = process_prices.ProcessPrices()
    price = "1 qt ($1.32/qt)"

    expected_output = round((1.32 / 32), 2)  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_quart(price) == expected_output


    # Add more test cases to cover different scenarios

def test_process_fl_oz():
    process = process_prices.ProcessPrices()
    price = "50 fl oz ($0.06/fl oz)"

    expected_output = 0.06  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_fl_ounces(price) == expected_output

    # Add more test cases as needed
    price_2 = "92 fl oz ($0.12/fl oz)"
    expected_output_2 = 0.12
    assert process.process_fl_ounces(price_2) == expected_output_2

    # Add more test cases as needed
    price_2 = "59 fl oz ($0.08/fl oz)"
    expected_output_2 = 0.12
    assert process.process_fl_ounces(price_2) == expected_output_2


    # Add more test cases to cover different scenarios

def test_process_fl_ea():
    process = process_prices.ProcessPrices()
    price = "12 x 50.7 fl oz ($1.25/ea)"

    expected_output = round((1.25 / 50.75), 2)   # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_fl_oz_ea(price) == expected_output

    # Add more test cases as needed
    price_2 = "12 x 12 fl oz ($0.33/ea)"
    expected_output_2 = round((0.33 / 12), 2)
    assert process.process_fl_oz_ea(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_process_oz_ea():
    process = process_prices.ProcessPrices()
    price = "2 x 4 oz ($0.95/ea)"

    expected_output = round((.95 / 4), 2)  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_oz_ea(price) == expected_output

    # Add more test cases as needed
    price_2 = "2 x 2 oz ($0.70/ea)"
    expected_output_2 = round((0.70 / 2), 2)
    assert process.process_oz_ea(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_process_lb_ea():
    process = process_prices.ProcessPrices()
    price = "32 x 1 lb ($0.92/ea)"

    expected_output = round((.92 / (1 * 16)), 2)  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_lb_ea(price) == expected_output

    # Add more test cases as needed
    price_2 = "5 x 2 lb ($0.70/ea)"
    expected_output_2 = round((0.70 / (2 * 16)), 2)
    assert process.process_lb_ea(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_process_mult_lb():
    process = process_prices.ProcessPrices()
    price = "10 lb ($1.70/lb)"

    expected_output = round((1.70 / 16), 2)  # Assuming this is the expected output based on the conversion table

    # Call the function and assert the output
    assert process.process_multi_lbs(price) == expected_output

    # Add more test cases as needed
    price_2 = "2 lb ($2.40/lb)"
    expected_output_2 = round((2.40 / 16), 2)
    assert process.process_multi_lbs(price_2) == expected_output_2

    # Add more test cases to cover different scenarios

def test_unit_price_data():
    webscrape = WebScraper()
    with open("grocery_data.json", "r") as file:
        data = json.load(file)

    items = data['18976']['Wegmans']["Items"]

    for key, value in items.items():
        for key_2, value_2 in value.items():
            print(value_2["price_per_ounce"])
            webscrape.process_unit_price_data(value_2["price_per_ounce"])

