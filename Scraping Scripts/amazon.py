from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium import webdriver


def main():
    amazonURL = str(input("Enter Amazon Product URL: "))
    # meeshoURL = str(input("Enter Meesho Product URL: "))
    # flipkartURL = str(input("Enter Flipkart Product URL: "))
    # myntraURL = str(input("Enter Myntra Product URL: "))
    # ajioURL = str(input("Enter Ajio Product URL: "))

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    # URL = "https://www.amazon.in/Swornof-Womens-Chanderi-Linen-Cottonlleave-8888_White/dp/B0B3XB5S8C/"

    driver = webdriver.Chrome()

    if amazonURL != "skip":

        amazon(amazonURL, driver)
    # if meeshoURL != "skip":
    #     meesho(meeshoURL, HEADERS, soup)
    # if flipkartURL != "skip":
    #     flipkart(flipkartURL, HEADERS, soup)
    # if myntraURL != "skip":
    #     myntra(myntraURL, HEADERS, soup)
    # if ajioURL != "skip":
    #     ajio(ajioURL, HEADERS, soup)



def amazon(URL, driver):
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "lxml")

    id = URL[URL.index('dp/')+3: URL.index('dp/')+13]
    print(id)
    print()

    title = soup.find("span", attrs={"id":'productTitle'})
    title_value = title.string
    title_string = title_value.strip()

    print(title_string)
    print()

    price = soup.find("span", attrs={"class":'a-price-whole'})
    print(price.text)
    print()

    seller = soup.find("a", attrs={"id":'bylineInfo'})
    print("https://www.amazon.in" + seller.get('href'))
    print()

    description = soup.find_all("ul", attrs={"class":'a-unordered-list a-vertical a-spacing-small'})
    desc_list = []
    desc_html_list = []
    for items in description:
        desc_html_list.append(items)
        desc_list.append(items.text)
    print(desc_list)
    print()
    print(desc_html_list)
    print()

    colour = soup.find("span", attrs={"class":'selection'}).text
    print(colour)
    print()

    images = soup.find_all('li', attrs={"class": 'a-spacing-small item imageThumbnail a-declarative'})
    img_list = []
    for ele in images:
        src = ele.find("img").get('src').strip()
        img_list.append(src)

    print(img_list)
    print()

    URL2 = URL

    variants = soup.find('ul', attrs={"class": 'a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesRectangle imageSwatches'}).findChildren("li", recursive=False)
    varaint_list = []
    for data in variants:
        variant_id = data.get('data-defaultasin')
        URL2.replace(id, variant_id)
        varaint_list.append(URL2)

    varaint_list.remove(URL)
    print(varaint_list)
    print(varaint_list.__len__())



main()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# webpage = requests.request("GET", URL, headers=HEADERS)

# soup = BeautifulSoup(webpage.content, "lxml")
# # print(soup.prettify())

# # Outer Tag Object
# title = soup.find("span", attrs={"id":'productTitle'})
# title_value = title.string
# title_string = title_value.strip()

# print("Product Title = ", title_string)

# price = soup.find("span", attrs={"class":'a-price-whole'})
# print(price)
# # price_value = price.string
# # price_string = price_value.strip()

# # print("Price Title = ", price_string)

# images = soup.find_all("span", attrs={"id":'a-autoid-3-announce'})
# for ele in images:
#     # print(ele)
#     src = ele.findChild("img").get('src')
#     print(src)

# title = driver.find_element(By.ID, "productTitle").text
# print(title)

# price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
# print(price)

# seller = driver.find_element(By.ID, "bylineInfo").get_attribute("href")
# print(seller)

# description = driver.find_elements(By.CLASS_NAME, "a-list-item.a-size-base.a-color-base")
# for items in description:
#     print(items.text)

# description = driver.find_elements(By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-small")
# for items in description:
#     print(items.text)

# description = driver.find_element(By.CLASS_NAME, "a-expander-content.a-expander-partial-collapse-content.a-expander-content-expanded").get_attribute("innerHTML")
# print(description)