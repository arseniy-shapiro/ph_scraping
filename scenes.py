from bs4 import BeautifulSoup
import requests


def scrape_page():

    url = "https://vvord.ru/tekst-filma/Scenyi-iz-supruzheskoy-zhizni/"
    
    with open("file.txt", "w") as file:

        for i in range(1, 25):
            if i != 1:
                page = url + str(i)
            else:
                page = url
            
            html_page = requests.get(page).text
            dom = BeautifulSoup(html_page, "lxml")
            page = dom.find("pre").text
            file.write(f"{page}\n\n")

            print(f"Скопирована страница {i}/24")

scrape_page()
