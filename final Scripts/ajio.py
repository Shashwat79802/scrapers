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
    folder = "ajio" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
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


def scrape_url(url, json_data):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    driver.quit()

    json_data = soup.find_all("script")
    for ele in json_data:
        if "window.__PRELOADED_STATE__ = " in ele.text:
            json_data = ele.text.strip()
            json_data = json_data[29:-1]
            break
    json_data = json.loads(json_data)

    id = url[url.index('/p/') + 3:]
    # print(id)
    # print(8)

    title = json_data['product']['productDetails']['name']
    # print(title)
    # print(9)

    price = json_data['product']['productDetails']['price']['value']
    # print(price)
    # print(10)

    seller = json_data['product']['productDetails']['brandName']
    # print(seller)
    # print(11)

    desc = '\n'
    description = json_data['product']['productDetails']['featureData']
    for data in description:
        desc += data['featureValues'][0]['value'] + '\n'
    # print(desc)


    colour = json_data['product']['productDetails']['baseOptions'][0]['options'][0]['color']

    image_divs = json_data['product']['productDetails']['images']
    img_list = []
    for img in image_divs:
        img_list.append(img['url'])
    # print(img_list)

    os.mkdir(id)
    # try:
    #     os.mkdir(id)
    # except FileExistsError:
    #     os.rmdir(id)
    #     os.mkdir(id)

    i = 0
    for link in img_list:
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
        'color': [colour],
        'description': [desc],
        'images': [img_list]
    }
    # print(data)

    df = pd.DataFrame(data)
    return df


def scrape_amazon():
    folder = "ajio" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    os.mkdir(folder)
    os.chdir(folder)

    flipkartURL = str(input("Enter Ajio URLs: "))
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

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        driver.quit()

        json_data = soup.find_all("script")
        for ele in json_data:
            if "window.__PRELOADED_STATE__ = " in ele.text:
                json_data = ele.text.strip()
                json_data = json_data[29:-1]
                break
        json_data = json.loads(json_data)

        id = json_data['product']['productDetails']['code']

        variant_list = []
        variants = json_data['product']['productDetails']['baseOptions'][0]['options']
        for vars in variants:
            url = flipkartURL.replace(id, vars['code'])
            variant_list.append(url)

        if len(variant_list) == 0:
            variant_list.append(flipkartURL)

        # print(variant_list)

        for url in variant_list:
            # print(7, url)
            try:
                df = scrape_url(url, json_data)
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
