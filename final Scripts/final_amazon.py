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
from selenium.webdriver.chrome.options import Options


def img_download(img_list):
    folder = "amazon" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
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


def repeat_img_scraper(url):
    chrome_options = Options()
    user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    images = soup.select('ul.regularAltImageViewLayout li.thumbItemUnrolled img')
    # print(images)
    # print()
    # print()
    # print()
    img_list = []
    for ele in images:
        # print(ele)
        src = ele.get('src')
        img_list.append(src)

    if (len(img_list) == 0):
        i = 1

        class_li = "thumbItemUnrolled thumbTypeimage thumbIndex0"
        while True:
            images = soup.find('li', attrs={"class": class_li})
            if images is None:
                break
            else:
                src = images.find("img").get('src')
                img_list.append(src)
                class_li = class_li[0:-1] + str(i)
                i += 1

    if (len(img_list) == 0):
        img_list = repeat_img_scraper(url)

    return img_list


def scrape_url(url):
    chrome_options = Options()
    user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    driver.quit()

    if 'gp/product' in url:
        url.replace('gp/product', 'dp')

    id = str(url[url.index('dp/')+3: url.index('dp/')+13])
    # print(id)
    # print(8)

    title = soup.find("span", attrs={"id":'productTitle'})
    title_value = title.string
    title_string = title_value.strip()
    # print(title_string)
    # print(9)

    price = soup.find("span", attrs={"class":'a-price-whole'}).text
    # print(price)
    # print(10)

    seller = soup.find("a", attrs={"id":'bylineInfo'}).get('href')
    # print("https://www.amazon.in" + seller.get('href'))
    # print(11)
    seller = "https://www.amazon.in" + seller
    # print(seller)

    description = soup.find_all("ul", attrs={"class":'a-unordered-list a-vertical a-spacing-small'})
    desc_list = []
    desc_html_list = []
    for items in description:
        desc_html_list.append(items)
        desc_list.append(items.text)
    # print(desc_list)
    # print(12)
    # print(desc_html_list)
    # print(13)

    json_data = soup.find_all("script", attrs={"type":'text/javascript'})
    for data in json_data:
        if "jQuery.parseJSON" in str(data):
            indexOfjquery = str(data).index("jQuery.parseJSON")+18
            endIndex = str(data).index("}');")+1
            json_data = str(data)[indexOfjquery:endIndex].strip()
            break

    json_data = json.loads(json_data)

    # try:
    #     colour = soup.find("span", attrs={"class":'selection'}).text
    # except AttributeError:
    #     colour = "No color"

    colour = json_data['landingAsinColor']
    # print(colour)
    # print(14)

    # images = soup.select('ul.regularAltImageViewLayout li.thumbItemUnrolled img')
    # # print(images)
    # # print()
    # # print()
    # # print()
    # img_list = []
    # for ele in images:
    #     # print(ele)
    #     src = ele.get('src')
    #     img_list.append(src)

    try:
        img_list = []
        images = json_data['colorImages'][colour]
        for img in images:
            try:
                img_list.append(img['hiRes'])
            except Exception as e:
                print(e)
                break
    except KeyError:
        json_data2 = soup.find_all("script", attrs={"type":'text/javascript'})
        for data in json_data2:
            if "'colorImages': { 'initial'" in str(data):
                indexOfjquery = str(data).index("colorImages': { 'initial'")+14
                endIndex = str(data).index(""",
                'colorToAsin': {'initial'""")
                json_data2 = str(data)[indexOfjquery:endIndex].strip()
                break
        json_data2 = json_data2.replace(" 'initial'", '"initial"')
        json_data2 = json.loads(json_data2)
        img_list = []

        for img in json_data2['initial']:
            img_list.append(img['large'])

        # print(img_list)

    # if (len(img_list) == 0):
    #     i = 1

    #     class_li = "thumbItemUnrolled thumbTypeimage thumbIndex0"
    #     while True:
    #         images = soup.find('li', attrs={"class": class_li})
    #         if images is None:
    #             break
    #         else:
    #             src = images.find("img").get('src')
    #             img_list.append(src)
    #             class_li = class_li[0:-1] + str(i)
    #             i += 1


    # if (len(img_list) == 0):
    #     img_list = repeat_img_scraper(url)
    # # print(15)

    try:
        os.mkdir(id)
    except FileExistsError:
        os.rmdir(id)
        os.mkdir(id)

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
        'title': [title_string],
        'price': [price],
        'seller': [seller],
        'color': [colour],
        'description': [description],
        'description_html': [desc_html_list],
        'images': [img_list]
    }
    # print(data)

    df = pd.DataFrame(data)
    return df


def scrape_amazon():
    folder = "amazon" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    os.mkdir(folder)
    os.chdir(folder)

    amazonURL = str(input("Enter Amazon URLs: "))
    output_file_name = str(input("Enter the output file name: "))
    # print(2)

    urlList = amazonURL.split(" ")
    # print(3, urlList)

    dfs = []

    for amazonURL in urlList:
        # print(4, "Scraping URL : ", amazonURL)
        # print()
        chrome_options = Options()
        user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
        )
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(amazonURL)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        driver.quit()

        variant_list = []

        if 'gp/product' in amazonURL:
            amazonURL = amazonURL.replace('gp/product', 'dp')

        id = amazonURL[amazonURL.index('dp/')+3: amazonURL.index('dp/')+13]
        # print(5, id)

        variants = None

        try:
            variants = soup.find('ul', attrs={"class": 'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesRectangle imageSwatches'}).findChildren("li")
            # print(variants)
            for data in variants:
                variant_id = data.get('data-defaultasin')
                URL2 = amazonURL.replace(id, variant_id)
                variant_list.append(URL2)
        except AttributeError:
            variant_list.append(amazonURL)
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
