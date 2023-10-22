from bs4 import BeautifulSoup
import gspread
import pandas as pd
import requests
from selenium import webdriver
import time

from classes import ProductPage, AllTopicsPage, TopicPage
from storage import StorageTank


# Product Hunt default path
MAIN_URL = "https://www.producthunt.com"

# Starting page with list of all topics
ALL_TOPICS_URL = f"{MAIN_URL}/topics"

# Set our goal Google Sheet
SPREADSHEET = "Копия Scraping format"
WORKSHEET = "Sample from PH"


def main():

    # Get full list of topics from the Product Hunt page
    all_topics = get_all_topics()
    number_of_topics = len(all_topics)

    # Keep track of how many topics program already parsed
    topic_counter = 0

    for topic in all_topics:
        # Get all products in every topic
        products = get_all_products_in_topic(topic)
        number_of_products = len(products)

        product_counter = 0

        for product in products:
            # Parse every product page
            parsed_page = parse_product_page(product)

            product_counter += 1
            print(f"Finished with product {product_counter}/{number_of_products}")

            # Make sure no errors occured
            if parsed_page:
                # Add info to the storage
                StorageTank().add_data(parsed_page)
        
        # Print how much work is to be done
        topic_counter += 1
        print(f"Finished with topic: {topic_counter}/{number_of_topics}")

    # Finally write all information to the google spreadsheet
    write_to_google_sheet()

    # Maybe try SQL and then SQL -> Google Sheet?
    # Maybe I should mesure executing time more accurate?
    
    print("Done working")
    return 0 


def write_to_google_sheet():
    '''Write whole data in given spreadsheet using Google Sheets API'''

    # Authorization
    servive_account = gspread.service_account(filename="service_account_key.json")

    # Get workseet
    worksheet = servive_account.open(SPREADSHEET).worksheet(WORKSHEET)

    # Transfer data to proper format
    data = pd.DataFrame.from_dict(StorageTank().data)

    # Write to worksheet
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())


def get_all_topics() ->list:
    '''Take page with all topics and get all their urls'''

    # Scroll the page to the end
    all_topics_page_scrolled = scroll_page(ALL_TOPICS_URL)

    # Get its full DOM
    dom = BeautifulSoup(all_topics_page_scrolled, "lxml")

    # Find all topics
    topics = dom.find_all(AllTopicsPage().topic["tag"], class_=AllTopicsPage().topic["class_name"])

    # Extract their urls
    return [f"{MAIN_URL}{topic.a['href']}" for topic in topics]


def get_all_products_in_topic(topic_url: str) -> list:
    '''Take topic page and pull all product urls'''

    # Scroll the page to the end
    topic_url_scrolled = scroll_page(topic_url)

    # Get its full DOM
    dom = BeautifulSoup(topic_url_scrolled, "lxml")

    # Find all products
    products = dom.find_all(TopicPage().product["tag"], class_=TopicPage().product["class_name"])
    product_urls = []

    for product in products:

        # Get path to product
        product_url = product.a["href"]

        # Make sure there is no repepition
        if StorageTank().avoid_repetition(product_url):

            # Add full url to the list
            product_urls.append(f"{MAIN_URL}{product_url}")

        else:
            print("repetition avoided")

    return product_urls
        
        
def scroll_page(url):
    '''Scroll down a page and return it in its full length'''

    # Set Google Chrome-driver
    driver = webdriver.Chrome()

    try:
        # Send GET request
        driver.get(url)
        
        # Set current scrolling height
        privious_height = driver.execute_script('return document.body.scrollHeight')

        while True:

            # Scroll down
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Wait two seconds to load new products
            time.sleep(2)

            # Get current scrolling height
            new_height = driver.execute_script('return document.body.scrollHeight')

            # Check if program reached the end of the page
            if new_height == privious_height:
                
                print("Reached end of the page")

                # Return full page
                return driver.page_source

            # Set new scrolling height
            privious_height = new_height

    except Exception as e:
        # In case of error print its type
        print(f"Exeption occurred: {e.__class__.__name__}")

    finally:
        driver.close()
        driver.quit()


def parse_product_page(url) ->dict:
    '''Pull all the necessary info from given product page'''
    
    # Send GET request
    try:
        html_page = requests.get(url).text

    # Catch all possible errors and exit if occured
    except requests.exceptions.RequestException:
        return False

    # Get HTML-DOM
    dom = BeautifulSoup(html_page, "lxml")

    # Create dict for future info
    result_dict = {"Source": url}

    # Get every needed param
    for column in ProductPage().columns:

        if column == "rating":
            
            try:
                # Get info
                info = dom.find(getattr(ProductPage(), column)["tag"], type=getattr(ProductPage(), column)["type"]).text

                # Get rating number only
                index_1, index_2 = info.find('"ratingValue":'), info.find('"worstRating"')
                info = info[index_1:index_2].replace('"ratingValue":"', '').rstrip('",')

                # Delete leading zero if needed
                if info[-1] == "0":
                    info = info[0]

            except (AttributeError, IndexError):
                # Case when there is no rating on a page
                info = ""
            else:
                info = f"{info}/5"

        elif column == "category":
            # There may be multiple categories
            try:
                info = dom.find_all(getattr(ProductPage(), column)["tag"], class_=getattr(ProductPage(), column)["class_name"])

                temp = "".join([f"{elem.text}, " for elem in info])
                info = temp.rstrip(", ")

            except Exception as e:
                print(f"Exeption occurred: {e.__class__.__name__} column = category")
                info = ""

        elif column == "link":
            # Get link and get rid of its unwanted path
            try:
                info = dom.find(getattr(ProductPage(), column)["tag"], class_=getattr(ProductPage(), 
                                    column)["class_name"])["href"].removesuffix("?ref=producthunt")
            except Exception as e:
                print(f"Exeption occurred: {e.__class__.__name__} column = link")
                return False

        else:
            # In other cases simply get info
            try:
                info = dom.find(getattr(ProductPage(), column)["tag"], class_=getattr(ProductPage(), column)["class_name"]).text

            except AttributeError:
                # In case of no info leave blank space or zero
                if column in ["reviews", "followers"]:
                    info = 0
                else:
                    info = ""
            else:
                if column == "reviews":
                    # Get rid of unwanted stuff
                    info = info.replace("reviews", "").replace("review", "")
        
                elif column == "followers":
                    # Get rid of unwanted stuff
                    info = info.replace("followers", "").replace("follower", "")

        # Fill in the created dict
        result_dict[column.capitalize()] = info

    return result_dict


if __name__ == "__main__":
    main()
