from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import json
import os
from PIL import Image
from io import BytesIO
from datetime import datetime



def img_download(img_list):
    folder = "meesho" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    try:
        os.mkdir(folder)
    except FileExistsError:
        os.rmdir(folder)
        os.mkdir(folder)
    os.chdir(folder)
    img_list = img_list.split(" ")
    i = 0
    print()
    for link in img_list:
        # print(link)
        response = requests.get(link)
        img = Image.open(BytesIO(response.content))
        img.save(str(i) + ".jpg")
        i += 1
        print("Image downloaded successfully : ", link)


def scrape_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    id = url.index("/p/")
    product_id = str(url[id + 3:])
    # print("id", product_id)
    # print()

    title = soup.find("title").text
    # print("title", title)
    # print()

    description = soup.find("meta").get("content")
    # print("description", description)
    # print()

    script = soup.find("script", attrs={"id": "__NEXT_DATA__"})
    dict = script.text
    dict = json.loads(dict)

    price = dict['props']['pageProps']['initialState']['product']['details']['data']['suppliers'][0]['price']
    # price = soup.find("div", attrs={"class": "sc-bcXHqe eWRWAb ShippingInfo__PriceRow-sc-frp12n-1 eMWeDN ShippingInfo__PriceRow-sc-frp12n-1 eMWeDN"}).find_next('h4').text
    # print("price", price)
    # print()

    # seller = soup.find("span", attrs={
        # "class": "sc-dkrFOg immaYJ ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu"}).text
    seller = dict['props']['pageProps']['initialState']['product']['details']['data']['suppliers'][0]['handle']
    # print(seller, "seller")
    # print()

    # images = soup.find("div", attrs={"class": "sc-bTTELM bjyqMe"}).findChildren("div", recursive=False)
    # img_list = []
    # for img in images:
    #     img_list.append(img.find("img").get("src"))
    img_list = dict['props']['pageProps']['initialState']['product']['details']['data']['images']
    # print("img_list", img_list)
    # print()

    try:
        os.mkdir(product_id)
    except FileExistsError:
        os.rmdir(product_id)
        os.mkdir(product_id)

    i = 0
    for link in img_list:
        # print(link)
        response = requests.get(link)
        img = Image.open(BytesIO(response.content))
        img.save(product_id + "/" + str(i) + ".jpg")
        i += 1



    colors = [
        "Black", "White", "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink",
        "Brown", "Gray", "Beige", "Cyan", "Teal", "Maroon", "Olive", "Lavender",
        "Violet", "Indigo", "Turquoise", "Magenta", "Salmon", "Peach", "Gold",
        "Silver", "Bronze", "Charcoal", "Burgundy", "Tan", "Cream", "Khaki", "Navy",
        "Mint", "Ruby", "Emerald", "Sapphire", "Amber", "Coral", "Ivory", "Lilac",
        "Mauve", "Mustard", "Plum", "Rose", "Rust", "Sky Blue", "Slate", "Taupe",
        "Apricot", "Aquamarine", "Celadon", "Cerulean", "Cobalt", "Coffee", "Copper",
        "Denim", "Ebony", "Eggplant", "Forest Green", "Fuchsia", "Ginger", "Granite",
        "Hazelnut", "Honey", "Jade", "Jasper", "Kelly Green", "Lemon", "Mahogany",
        "Mandarin", "Midnight Blue", "Obsidian", "Onyx", "Opal", "Peacock Blue",
        "Periwinkle", "Pine Green", "Pistachio", "Pumpkin", "Raspberry", "Royal Blue",
        "Saffron", "Sepia", "Sienna", "Smoke", "Snow", "Steel Blue", "Tangerine",
        "Topaz", "Ultramarine", "Vermilion", "Wine", "Zaffre"
    ]

    color = 0
    for item in colors:
        if item.lower() in title.lower().split(" "):
            color = item
            break
    # print("color", color)
    # print()

    data = {
        'product_id': [product_id],
        'Product URL': [url],
        'title': [title],
        'price': [price],
        'seller': [seller],
        'color': [color],
        'description': [description],
        'images': [img_list]
    }
    # print(data)
    # print("--------------------------------------------------------------------------------------------------------")
    # print()
    # print()

    df = pd.DataFrame(data)

    driver.quit()

    return df


def scrape_meesho():
    folder = "meesho" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    os.mkdir(folder)
    os.chdir(folder)

    meeshoURL = str(input("Enter Meesho URLs: "))
    output_file_name = str(input("Enter the output file name: "))
    print()

    urlList = meeshoURL.split(" ")
    # print(urlList)

    dfs = []

    for meeshoURL in urlList:
        print("Scraping URL : ", meeshoURL)
        print()
        driver = webdriver.Chrome()
        driver.get(meeshoURL)
        soup = BeautifulSoup(driver.page_source, "lxml")

        variant_list = []

        variants = soup.find_all("div", attrs={"class": "sc-ZqFbI kzaKJz"})
        for variant in variants:
            variant_list.append("https://www.meesho.com" + variant.findChild('a').get("href"))


        for url in variant_list:
            # print(meeshoURL)
            try:
                df = scrape_url(url)
                dfs.append(df)
                print("URL scraped successfully : ", url)
            except AttributeError:
                # exit()
                print("URL scraping failed, will try again : ", url)
                variant_list.append(url)

        # print(dfs)
        result_df = pd.concat(dfs, ignore_index=True)
    result_df.to_excel(output_file_name+'.xlsx', index=False)



while True:
    print()
    choice = int(input("Enter 1 to scrape data from URLs or 2 to download image from URLs: "))

    if choice == 2:
        URLs = str(input("Enter URLs: "))
        img_download(URLs)
        print("---------------------------Images downloaded successfully---------------------------")
    elif choice == 1:
        scrape_meesho()
        print()
        print("---------------------------Data scraped successfully---------------------------")
    else:
        print("Wrong choice")
