# KongoScrapper

**KongoScrapper** is a scraper built in Python that extracts product information from the site kingofthekongo.com.ar, saving the data in structured .json files. This project can be useful for price analysis, stock monitoring, product comparisons, or other automated purposes.

---

## 🚀 ¿What does it do?
- Navigate through all site sections. 
- Extracts the section title and listed products.
- For each product, it obtains:
  - Name
  - Price
  - Image
- Saves all data in the folder `data/` with JSON format.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/tuusuario/KongoScrapper.git
cd KongoScrapper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Main Requirements:
> - `requests`
> - `beautifulsoup4` 

3. Run main script:

```python
from kongo_scrapper import KongoScrapper

scraper = KongoScrapper()
scraper.start_scrapping(clean_files=True)  # Set clean_files=True if you want delete all files from 'data'
```

> All `.json` files will be save in `/data` folder.

---

## 📄 Example: 

```json
{
  "title": "Remerones - King of the Kongo",
  "products": [
    {
      "name": "Remeron Verified Grey",
      "price": "$57.990",
      "photo": "https://acdn-us.mitiendanube.com/stores/219/431/products/a...jpg"
    },
    {
      "name": "Remeron Teddy Mnky",
      "price": "$44.990",
      "photo": "https://acdn-us.mitiendanube.com/stores/219/431/products/e...jpg"
    }
  ]
}
```

## 📬 Contact

[LinkedIn](https://linkedin.com/in/mateo-giuffra-023682289/) • [Gmail](mailto:matteogiuffrah40@gmail.com)

> For any questions, doubts, or if you'd just like to reach out, feel free to use either of the contacts above.
