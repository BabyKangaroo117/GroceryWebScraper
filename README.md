## How to Run the Web Scraper

### Activate environment
- In the terminal if poetry is not installed write: pip install poetry
- cd to the following path ../GroceryWebscraper/GroceryScraper
	- cd GroceryScraper
- Use the command: poetry shell
- Environment is now activated
### Run the Web Scraper
- Go to the groceryscraper folder
- Open main.py
- Run main.py and the web scrapers will start
- The Wegmans scraper is in headless mode so it till take a few seconds before data starts printing
- The Shoprite Web Scraper has to open a new chrome tab for each search to avoid bot detection
### Data
- Data is saved in the grocery_data folder in json files
- Data is only saved if the webs scraper successfully runs through all the items in the grocery list


## Issues
- The API is not having successful calls to the database. We are able to send successful payloads through swagger, but get error 500 through python with the same payload
- Data has to be converted to a list of tuples with the data for each attribute in the AreaItems table
- All the data is deleted in AreaItems, then an insert statement is used add all the items

## Cheapest Price Data
- Comment out the webscrapers in main.py
- Run the format_for_sql_insert() function

## CI
- GitHub Workflows is used to run pytest when there is a push or pull request from master
- There are many more tests that need to be written, but the structure for the workflow is set up