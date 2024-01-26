import time
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def img_download(img_list):
    folder = "flipkart" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    try:
        os.mkdir(folder)
    except FileExistsError:
        os.rmdir(folder)
        os.mkdir(folder)
    os.chdir(folder)
    img_list = img_list.split(" ")
    i = 0
    # print()
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
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    driver.quit()

    id = str(url[url.index('/p/')+3: url.index("?")])
    # print(id)
    # print(8)

    title = soup.find("meta", attrs={"name":'Keywords'})
    title = title.get('content')
    # print(title)
    # print(9)
    

    price = soup.find("div", attrs={"class":'_30jeq3 _16Jk6d'}).text
    # print(price)
    # print(10)

    seller = soup.find("span", attrs={"class":'G6XhRU'}).text
    # print(seller)
    # print(11)

    description = soup.find("div", attrs={"class":'X3BRps'})
    # print(desc_list)
    # print(12)
    # print(desc_html_list)
    # print(13)

    
    colour = soup.find("span", attrs={"class":'B_NuCI'}).text.lower()
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
        if item.lower() in colour:
            color = item
            break
    # print(color)
    # print(14)

    list_img = []
    images_list = soup.find('ul', attrs={"class": '_3GnUWp', "style": "transform: translateY(0px);"})
    images = images_list.findChildren("li")
    for img in images:
        src = img.find("img").get('src')
        src = src.replace("128/128", "832/832")
        list_img.append(src)
    # print(list_img)

    try:
        os.mkdir(id)
    except FileExistsError:
        os.rmdir(id)
        os.mkdir(id)

    i = 0
    for link in list_img:
        # print(link)
        response = requests.get(link)
        img = Image.open(BytesIO(response.content))
        img.save(id + "/" + str(i) + ".jpg")
        i += 1

    data = {
        'product_id': [id],
        'Product URL': [url],
        'title': [title],
        'price': [price],
        'seller': [seller],
        'color': [color],
        'description': [description.text],
        'description_html': [description],
        'images': [list_img]
    }
    # print(data)

    df = pd.DataFrame(data)
    return df


def scrape_amazon():
    folder = "flipkart" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    os.mkdir(folder)
    os.chdir(folder)

    flipkartURL = str(input("Enter Flipkart URLs: "))
    output_file_name = str(input("Enter the output file name: "))
    # print(2)

    urlList = flipkartURL.split(" ")
    # print(3, urlList)

    dfs = []

    for flipkartURL in urlList:
        # print(4, "Scraping URL : ", amazonURL)
        # print()
        driver = webdriver.Chrome()
        driver.get(flipkartURL)


        try:
            more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_3F0T5D.vvSfKl._11HRc7")))
            more_button.click()
            time.sleep(3)
        except:
            print("More button not found")

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        driver.quit()

        variant_list = []

        a_tags = soup.select('li._3V2wfe a.kmlXmn')
        variant_list = ["https://www.flipkart.com" + a['href'] for a in a_tags]
        # print(variant_list)
        # print(6, variant_list)

        for url in variant_list:
            # print(7, url)
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
    os.chdir("..")


while True:
    # print(1)
    choice = int(input("Enter 1 to scrape data from URLs or 2 to download image from URLs: "))

    if choice == 2:
        URLs = str(input("Enter URLs: "))
        img_download(URLs)
        print("---------------------------Images downloaded successfully---------------------------")
    elif choice == 1:
        scrape_amazon()
        print()
        print("---------------------------Data scraped successfully---------------------------")
    else:
        print("Wrong choice")
