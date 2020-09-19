from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.message import EmailMessage
from configs import EMAIL_ADDRESS, EMAIL_PASSWORD


def get_product_info(driver):
    title_id = "productTitle"
    price_id = "priceblock_ourprice"
    image_url_id = "landingImage"

    product_title = driver.find_element_by_id(title_id).text
    product_price = driver.find_element_by_id(price_id).text[1:]
    product_image_url = driver.find_element_by_id(image_url_id).get_attribute('src')

    return {
        "title": product_title,
        "price": product_price,
        "img_url": product_image_url
    }


def send_email(product):

    msg = EmailMessage()
    msg['Subject'] = "Amazon Price Tracker Notification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.add_alternative("""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>Your featured product is under $""" + MAX_PRICE + """. Don't miss it out!</h2>
                <ul>
                  <li><b>Name:</b> """ + product["title"] + """</li>
                  <li><b>Price:</b> $""" + product["price"] + """</li>
                  <li><b>URL:</b> """ + URL + """</li>
                </ul> 
                <img src='""" + product["img_url"] + """' width="300" height="250">
                <h2>Curious Coding</h2>
                <p>Visit my <a href="https://www.youtube.com/channel/UCfN908-BJ5xTCLGhJJpOJcA/">YouTube Channel</a></p>
            </body>
        </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == '__main__':

    CHROMEDRIVER = "/path/to/chromedriver"
    URL = "https://www.amazon.com/Canon-M200-EF-M-15-45mm-Black/dp/B07XYPVFCH/"
    MAX_PRICE = '600'

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
    driver = webdriver.Chrome(CHROMEDRIVER)
    driver.get(URL)

    product_info = get_product_info(driver)

    if float(product_info["price"]) <= float(MAX_PRICE):
        send_email(product_info)
