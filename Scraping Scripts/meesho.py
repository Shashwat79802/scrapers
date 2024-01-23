from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.by import By
from selenium import webdriver


meeshoURL = "https://www.meesho.com/jivika-pretty-sarees/p/3yhf09"
# meeshoURL = "https://www.meesho.com/pure-bright-red-colour-gold-toned-beautiful-trendy-banarasi-silk-woven-designer-saree/p/78hkk"
# meeshoURL = "https://www.meesho.com/s/p/uls7x?utm_source=s_cc"

driver = webdriver.Chrome()

driver.get(meeshoURL)
# print(driver.page_source)
soup = BeautifulSoup(driver.page_source, "lxml")



script = soup.find("script", attrs={"id": "__NEXT_DATA__"})
dict = script.text
dict = json.loads(dict)
print(type(dict))
print()
print(dict['props']['pageProps']['initialState']['product']['details']['data']['images'])
print()
print()
print()

images = soup.find("div", attrs={"class": "sc-bTTELM bjyqMe"}).findChildren("div", recursive=False)
img_list = []
for img in images:
    img_list.append(img.find("img").get("src"))
    # print()

print(img_list)
print()
exit()


id = meeshoURL.index("/p/")
print(meeshoURL[id+3:id+8])

title = soup.find("title").text
print(title)
print()

description = soup.find("meta").get("content")
print(description)
print()
# exit()

# title = soup.find("span", attrs={"class": "sc-dkrFOg kwVauV"})
# print(title.text)
# print()

try:
    price = soup.find("h4", attrs={"class": "sc-dkrFOg dAtHep"}).text
except AttributeError:
    price = soup.find("h4", attrs={"class": "sc-gKPRtg kUTRRv"}).text
print(price.removeprefix("₹"))
print()

# description = soup.find("div", attrs={"class": "sc-bcXHqe kMGMZD ProductDescription__DetailsCardStyled-sc-1l1jg0i-0 eFKyvM ProductDescription__DetailsCardStyled-sc-1l1jg0i-0 eFKyvM"}).find_all("p")
# description_list = []
# for data in description:
#     description_list.append(data.text)
#     # print()

# print(description_list)
# print()

seller = soup.find("span", attrs={"class": "sc-dkrFOg immaYJ ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu ShopCardstyled__ShopName-sc-du9pku-6 bdcHGu"})
print(seller.text)
print()

images = soup.find("div", attrs={"class": "sc-bTTELM bjyqMe"}).findChildren("div", recursive=False)
img_list = []
for img in images:
    img_list.append(img.find("img").get("src"))
    # print()

print(img_list)
print()


script = soup.find("script", attrs={"id": "__NEXT_DATA__"})
dict = script.text
print(type(dict))

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

if color != 0:
    print(color)
else:
    print("Color not found")
print()


variants = soup.find_all("div", attrs={"class": "sc-ZqFbI kzaKJz"})
variant_list = []
for variant in variants:
    variant_list.append("https://www.meesho.com" + variant.findChild('a').get("href"))

print(variant_list)
print()