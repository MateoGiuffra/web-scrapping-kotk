from bs4 import BeautifulSoup
import requests
import json 
import re 
class KongoScrapper: 
  
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    def get_link(self, url):
        new_url = ""
        for c in url: 
            if "jpg" in new_url:
                break
            new_url += c 
        return f"https:{new_url}"            
        
    def get_photo_link(self, url_product):
        response = requests.get(url_product, headers=self.HEADERS)
        if response.status_code != 200:
            return "https://acdn-us.mitiendanube.com/stores/219/431/products/b9b5d26a-6bd8-4ea2-99ed-1b310f5afd88-bc1182939b9ef3d10017335163465524-240-0.jpg"
        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img", "js-item-image")
        return self.get_link(img["data-srcset"])
    
    def get_price(self, price):
        pattern = r'\d+(?:\.\d+)?'
        numeros = re.findall(pattern , price)
        return f"${numeros[0]}"
    
    def get_product(self, item):
        price = item.find("span", class_="js-price-display").text
        format_price = self.get_price(price)
        name = item.find("div", class_="js-item-name").text
        url_product = item["href"]
        
        photo = self.get_photo_link(url_product)
        return {
            "name": name, 
            "price":format_price,
            "photo": photo
        }

    def start_scrapping(self, url):
        try:
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code != 200:
                return 

            print("Peticion exitosa")
            
            scrap = {
                "title": "",
                "products":[
                    {  
                    },
                ]
            }
            
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.title 
            if title_tag: 
                scrap["title"] = title_tag.text

            items = soup.find_all("a", class_="item-link")

            for item in items: 
                scrap["products"].append(self.get_product(item))

            return json.dumps(scrap, indent=2)
        except Exception as e:
            print(f"Something was wrong {e}")
            return {
                "error": "Somewhing was wrong: {e}" 
            }



if __name__ == "__main__":
    URL = 'https://kingofthekongo.com.ar/shop/prendas1/remeras-y-boxy/?mpage=3'
    # URL = 'https://kingofthekongo.com.ar/shop/prendas1/remerones/'
    scrapper = KongoScrapper()
    page = scrapper.start_scrapping(URL)
    print(page)