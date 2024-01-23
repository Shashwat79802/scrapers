from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import json

meeshoURL = str(input("Enter Meesho URL: "))
output_file_name = str(input("Enter the output file name: "))

variant_list = []


def scrape_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    id = url.index("/p/")
    product_id = url[id + 3:]
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


driver = webdriver.Chrome()
driver.get(meeshoURL)
soup = BeautifulSoup(driver.page_source, "lxml")

variants = soup.find_all("div", attrs={"class": "sc-ZqFbI kzaKJz"})
for variant in variants:
    variant_list.append("https://www.meesho.com" + variant.findChild('a').get("href"))

dfs = []
scrape_error = True
# while scrape_error:
#     scrape_error = False
#     for meeshoURL in variant_list:
#         try:
#             df = scrape_url(meeshoURL)
#             dfs.append(df)
#             result_df = pd.concat(dfs, ignore_index=True)
#             result_df.to_excel('output.xlsx', index=False)
#         except AttributeError:
#             scrape_error = True
#             break

for meeshoURL in variant_list:
    # print(meeshoURL)
    try:
        df = scrape_url(meeshoURL)
        dfs.append(df)
        print("URL scraped successfully : ", meeshoURL)
    except AttributeError:
        # exit()
        print("URL scraping failed, will try again : ", meeshoURL)
        variant_list.append(meeshoURL)

    # df = scrape_url(meeshoURL)
    # dfs.append(df)
    # result_df = pd.concat(dfs, ignore_index=True)
    # result_df.to_excel('output.xlsx', index=False)
    # variant_list.remove(meeshoURL)

# print(dfs)
result_df = pd.concat(dfs, ignore_index=True)
result_df.to_excel(output_file_name+'.xlsx', index=False)
