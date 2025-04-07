from bs4 import BeautifulSoup
import requests
import json 
import re 
from shutil import rmtree
import os 
class KongoScrapper: 
  
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    KONGO_URL = "https://kingofthekongo.com.ar/"
    DEFAUL_PRICE = "$65.565"
    DEFAULT_PHOTO_LINK = "https://acdn-us.mitiendanube.com/stores/219/431/products/b9b5d26a-6bd8-4ea2-99ed-1b310f5afd88-bc1182939b9ef3d10017335163465524-240-0.jpg"
    DEFAULT_TITLE = " UNTITLED"
    
    def __init__(self):
        self.good_requests = 0

    def get_link(self, urls):
        pattern = r"//[-\w+./]+"
        match = re.findall(pattern, urls)
        return f"https:{match[-1]}"          
        
    def get_photo_link(self, url_product):
        response = requests.get(url_product, headers=self.HEADERS)
        if response.status_code != 200:
            print("No image found, using default")
            return self.DEFAULT_PHOTO_LINK 
        
        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img", "js-item-image")
        
        if not img:
            print("No image found, using default")
            return self.DEFAULT_PHOTO_LINK
        
        possibles_links = img["data-srcset"]
        return self.get_link(possibles_links)
    
    def get_price(self, price):
        return price.strip() if price.strip() else self.DEFAULT_PRICE
    
    def get_product(self, item):
        price = item.find("span", class_="js-price-display").text
        format_price = self.get_price(price)
        name = item.find("div", class_="js-item-name").text
        product_url = item["href"]
        
        photo_link = self.get_photo_link(product_url)
        return {
            "name": name, 
            "price":format_price,
            "photo": photo_link
        }
           
    def get_file_title(self, title):
        try:
            pattern = r"[A-Z]+"
            match = (re.search(pattern, title[1:]))
            return match.group() if match else self.DEFAULT_TITLE
        except Exception as e: 
            print(f"Something was wrong while get_file_title {e}")
            return self.DEFAULT_TITLE
            
    def start_scrapping_of(self, url):
        try:
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code != 200:
                return 
            self.good_requests += 1
            scrap = {
                "title": self.DEFAULT_TITLE,
                "products":[]
            }
            
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.title 
            if title_tag: 
                scrap["title"] = title_tag.text

            items = soup.find_all("a", class_="item-link")

            for item in items: 
                scrap["products"].append(self.get_product(item))
            return scrap
        except Exception as e:
            print(f"Something was wrong {e}")
            return {
                "error": "Somewhing was wrong: {e}" 
            }

    def get_all_links(self):
        response = requests.get(self.KONGO_URL, headers=self.HEADERS)
        if response.status_code != 200:
            return 
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        items = soup.find_all("a", class_="nav-list-link")
        for i in items:
            try:
                link = i["href"]
                if link: 
                    links.append(link)
                    print(link) 
            except:
                continue
        return links 
    
    def delete_data_files(self):
        try: 
            rmtree("data/")
            os.mkdir("./data")
        except FileNotFoundError:
            os.mkdir("./data")    
        
    def start_scrapping(self, clean_files=False):
        if clean_files: 
            self.delete_data_files()
        self.good_requests = 0
        URLs = self.get_all_links()
        if not URLs:
            print("There aren't links.")
            return
        
        for i, url in enumerate(URLs):
            try:  
                scrap = self.start_scrapping_of(url)
                file_title = self.get_file_title(scrap["title"])
                with open(f"data/{file_title}.json", "x") as f:
                    json.dump(scrap, f, indent=2)
            except FileExistsError: 
                with open(f"data/{file_title + str(i)}.json", "x") as f:
                    json.dump(scrap, f, indent=2)
            except Exception as e: 
                print(f"Something was wrong while start_scrapping: {e}")
                continue
        print(f"Amount of Successful Requests: {self.good_requests}")
    

            
# if __name__ == "__main__": 
#     scrapper = KongoScrapper()
#     scrapper.start_scrapping()

# text = "//acdn-us.mitiendanube.com/stores/219/431/products/0809c78d-5d50-45bb-9070-3cb9f750505f-d6bba9ad356afedd6217346294756349-240-0.jpg 240w, //acdn-us.mitiendanube.com/stores/219/431/products/0809c78d-5d50-45bb-9070-3cb9f750505f-d6bba9ad356afedd6217346294756349-320-0.jpg 320w, //acdn-us.mitiendanube.com/stores/219/431/products/0809c78d-5d50-45bb-9070-3cb9f750505f-d6bba9ad356afedd6217346294756349-480-0.jpg 480w, //acdn-us.mitiendanube.com/stores/219/431/products/0809c78d-5d50-45bb-9070-3cb9f750505f-d6bba9ad356afedd6217346294756349-640-0.jpg 640w, //acdn-us.mitiendanube.com/stores/219/431/products/0809c78d-5d50-45bb-9070-3cb9f750505f-d6bba9ad356afedd6217346294756349-1024-1024.jpg 1024w"
title = "titlePage"
pattern = r"[A-Z]+"
match = (re.search(pattern, title[1:]))
print(match.group()) if match else print("nada")