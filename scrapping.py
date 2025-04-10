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
           
            
    def start_scrapping_of(self, url):
        try:
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code != 200:
                print("Status code error", response.status_code)
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
            print(f"Something was wrong while start_scrapping_of {e}")
            
    
    def create_new_file(self, folder_name, file_name, content):
        try: 
            with open(f"data/{folder_name}/{file_name}.json", "x") as f:
                    json.dump(content, f, indent=2)
        except FileNotFoundError: 
            os.mkdir(f"data/{folder_name}")
            with open(f"data/{folder_name}/{file_name}.json", "x") as f:
                    json.dump(content, f, indent=2)
        except FileExistsError as last_file:
            pattern = r"\d+"
            actual_number = int((re.search(pattern, last_file.filename)).group())
            next_number = str(actual_number + 1).zfill(3)
            file_name = f"{folder_name}-{next_number}"
            self.create_new_file(folder_name, file_name, content) 

    def get_title_of(self, page_title):
        try: 
            if "%" in page_title: 
                return "DESCUENTOS"
            pattern = r"[A-Z]+"
            match = re.search(pattern, page_title[1:])
            if not match: 
                return self.DEFAULT_TITLE
            return match.group()
        except Exception as e: 
            print("Someting was wrong while get_title_of",e)
            return self.DEFAULT_TITLE
    
    
    def add_new_file(self, scrap):
        try:
    
            folder_name = self.get_title_of(scrap["title"] )
            file_name = f"{folder_name}-000"
            self.create_new_file(folder_name, file_name, scrap)
        except Exception as e: 
            print(f"Something was wrong while get_file_title {e}")
        
    def get_all_products_links(self):
        response = requests.get(self.KONGO_URL, headers=self.HEADERS)
        if response.status_code != 200:
            return 
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        items = soup.find_all("a", class_="nav-list-link")
        for i in items:
            try:
                link = i["href"]
                if link and any(word in link for word in ("shop", "new", "sale", "mujer")): 
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
        
    def start_scrapping(self, clean_files=False, URLs=None):
        if clean_files: 
            self.delete_data_files()
        self.good_requests = 0
        URLs = self.get_all_products_links() if not URLs else URLs
        if not URLs:
            print("There aren't links.")
            return
        for url in URLs:
            try:  
                scrap = self.start_scrapping_of(url)
                self.add_new_file(scrap)
            except Exception as e: 
                print(f"Something was wrong while start_scrapping: {e}")
                continue
        print(f"Amount of Successful Requests: {self.good_requests}")
    

            
if __name__ == "__main__": 
    scrapper = KongoScrapper()
    scrapper.start_scrapping(clean_files=True)
    