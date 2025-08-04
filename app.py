from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scrape')
def scrape_books():
    url = 'http://books.toscrape.com/index.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    items = soup.find_all('article', class_='product_pod')

    for item in items:
        title_element = item.find("h3").find("a")
        price_element = item.find('p', class_='price_color')
        availability_element = item.find('p', class_='instock availability')

        title = title_element.get('title') if title_element else 'No title'
        price = price_element.get_text(strip=True) if price_element else 'No price'
        availability = availability_element.get_text(strip=True) if availability_element else 'No availability'
        books.append({
            'title': title,
            'price': price,
            'availability': availability
        })

    df = pd.DataFrame(books)

    return render_template('index.html', books=df.to_html(classes='table table-striped', index=False))

if __name__ == '__main__':

    app.run(debug=True, port=5000)

