# Ecommerce-scraping

This script scans e-commerce sites, capturing information about products for sale.
The average price and quantity of processed items are considered for the final result.

The objective of this project is to compare prices between sites in a simple way, the values ​​obtained
are stored in data frames that can be exported to Exel or csv, but are usually processed in a
summarized form for generating graphics.

Currently, 3 output graphics are generated:
<ol>
    <li>Relation between the quantity of items obtained (pizza)</li>
    <li>Comparison between average prices (bars)</li>
    <li>Average price per survey (plot)</li>
</ol>


It is not recommended to only consider the statistics of this script.
Unwanted products can unbalance the average final price in some cases.

To compile the code correctly, you must install the project dependencies listed below.
in addition to the Chrome browser. In case of incompatibility of the chromedriver with your
browser version, download the appropriate version from [chromium.org](https://chromedriver.chromium.org/downloads)
and replace the file in the script folder.

### Install dependencies (packages):
* `pip install pyautogui`
* `pip install selenium`
* `pip install matplotlib`
* `pip install pandas`
* `pip install bf4`

### Sites scraped by the script:
* Amazon
* Shopee

To avoid errors, do not interact with your machine at runtime.
Please report any errors with code execution.