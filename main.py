import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    product_name = ''
    product_price = ''
    rating = ''
    num_reviews = ''

    product_name_elem = soup.select_one('.a-size-medium')
    if product_name_elem:
        product_name = product_name_elem.get_text(strip=True)

    product_price_elem = soup.select_one('.a-price-whole')
    if product_price_elem:
        product_price = product_price_elem.get_text(strip=True)

    rating_elem = soup.select_one('.a-icon-alt')
    if rating_elem:
        rating = rating_elem.get_text(strip=True).split(' ')[0]

    num_reviews_elem = soup.select_one('.a-size-base')
    if num_reviews_elem:
        num_reviews = num_reviews_elem.get_text(strip=True)


    description = soup.select_one('#productDescription')
    asin = soup.select_one('[data-asin]')['data-asin'] if soup.select_one('[data-asin]') else ''
    product_description = soup.select_one('.a-section.a-text-left span', attrs={'class': 'a-list-item'}).get_text(strip=True) if soup.select_one('.a-section.a-text-left span', attrs={'class': 'a-list-item'}) else ''
    manufacturer = soup.select_one('#bylineInfo').get_text(strip=True) if soup.select_one('#bylineInfo') else ''

    return {
        'Product URL': url,
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating': rating,
        'Number of Reviews': num_reviews,
        'Description': description.get_text(strip=True) if description else '',
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }


base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

product_data = []


num_pages = 20
for page in range(1, num_pages + 1):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    product_links = soup.select('.s-result-item a.a-link-normal')
    for link in product_links:
        product_url = link['href']
        if product_url.startswith('/'):
            product_url = urljoin(url, product_url)
            product_data.append(scrape_product_details(product_url))


df = pd.DataFrame(product_data)

 
df.to_csv('product_data.csv', index=False)
