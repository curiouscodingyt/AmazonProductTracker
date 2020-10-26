from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests_html import HTML
import time
import re
import datetime
import pandas as pd


def scrape_product(url):
    """Scrape Amazon Product - Get Product price and title
    :param url: String
    :return: json
    """
    driver.get(url)
    time.sleep(0.5)

    title_id = "productTitle"
    price_id = "priceblock_ourprice"

    product_title = driver.find_element_by_id(title_id).text
    product_price = driver.find_element_by_id(price_id).text

    return {
        "price": product_price,
        "title": product_title
    }


def get_product_id_from_url(url):
    """"Get Amazon Product ID from product URL
    :param url: String
    :return: String
    """
    product_id = None
    for regex_option in regex_options:
        regex = re.compile(regex_option)
        match = regex.match(url)
        if match:
            try:
                product_id = match["product_id"]
            except:
                pass
    return product_id


def scrape_category(products=[]):
    """Scrape Amazon Category
    :param products: array of strings
    :return: json
    """

    scraped_data = []
    for product in products:
        product_url = product["url"]
        product_id = product["product_id"]
        product_data = {"title": None, "price": None}
        try:
            product_data = scrape_product(product["url"])
        except:
            pass

        scraped_data.append({
            "product_url": product_url,
            "product_id": product_id,
            "product_price": product_data["price"],
            "product_title": product_data["title"],
            "category": category["name"],
            "timestamp": datetime.datetime.now().timestamp()
        })

    return scraped_data


if __name__ == '__main__':

    # Initiate Chrome Driver
    CHROME_DRIVER = "/path/to/chromedriver"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(CHROME_DRIVER, options=options)

    # Define categories to scrape
    categories = [
        {"name": "toys-and-games", "url": "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/"}
    ]

    # Regular Expressions
    regex_options = [
        r"https://www.amazon.com/(?P<slug>[\w-]+)/dp/(?P<product_id>[\w-]+)/",
        r"https://www.amazon.com/dp/(?P<product_id>[\w-]+)/",
        r"https://www.amazon.com/gp/product/(?P<product_id>[\w-]+)/"
    ]

    for category in categories:
        # Get Links
        driver.get(category["url"])
        body_el = driver.find_element_by_css_selector("body")
        html_str = body_el.get_attribute("innerHTML")
        html_obj = HTML(html=html_str)
        # html_obj.links

        # Clean Links
        product_links = [link for link in html_obj.links if link.startswith("/")]
        product_links = [f"https://www.amazon.com{link}" for link in product_links]
        products = [{"product_id": get_product_id_from_url(link), "url": link} for link in product_links if get_product_id_from_url(link)]

        # Scrape products within a category
        final_data = scrape_category(products)

        # Save data to CSV
        final_data_df = pd.DataFrame(final_data)
        final_data_df.to_csv("categories.csv", index=False)

