# KongoScrapper

**KongoScrapper** es un scraper hecho en Python que extrae información de productos del sitio [kingofthekongo.com.ar](https://kingofthekongo.com.ar/), guardando los datos en archivos `.json` estructurados. Este proyecto puede ser útil para análisis de precios, control de stock, comparadores u otros fines automatizados.

---

## 🚀 ¿Qué hace?
- Navega por todas las secciones del sitio.
- Extrae el título de la sección y los productos listados.
- Por cada producto obtiene:
  - Nombre
  - Precio
  - Imagen
- Guarda los datos en formato JSON en la carpeta `data/`.

---

## ⚙️ Instalación y uso

1. Cloná el repositorio:

```bash
git clone https://github.com/tuusuario/KongoScrapper.git
cd KongoScrapper
```

2. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

> Requisitos principales:
> - `requests`
> - `beautifulsoup4` 

3. Ejecutá el script principal:

```python
from kongo_scrapper import KongoScrapper

scraper = KongoScrapper()
scraper.start_scrapping(clean_files=True)  # Pone clean_files=True si querés eliminar archivos anteriores
```

> Todos los archivos `.json` se guardarán en la carpeta `/data`.

---

## 📄 Ejemplo de salida

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

## 📬 Contacto

[LinkedIn](https://linkedin.com/in/mateo-giuffra-023682289/) • [Gmail](mailto:matteogiuffrah40@gmail.com)

> Cualquier consulta, duda o simplemente querés contactarme, podés usar alguno de los dos medios de arriba.
