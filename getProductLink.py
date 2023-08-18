import requests
import json
from bs4 import BeautifulSoup

def extract_product_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = []
        
        product_elements = soup.find_all('a', class_='find_tile__productLink')
        for product_element in product_elements:
            product_link = product_element.get('href')
            
            try:
                brand_element = product_element.find_next('span', class_='find_tile__brandInName')
                brand_name = brand_element.get_text()
                
                product_info.append({
                    'href': product_link,
                    'brand_name': brand_name
                })
            except AttributeError:
                print("Skipping URL:", url, "- Brand element not found")
                continue
            
        return product_info
    else:
        return []

if __name__ == '__main__':
    with open('product_records.json', 'r') as json_file:
        records = json.load(json_file)

    product_info_list = []

    for record in records:
        url = record['url']
        product_info = extract_product_info(url)
        product_info_list.extend(product_info)

    with open('product_info.json', 'w') as json_file:
        json.dump(product_info_list, json_file, indent=4)

    print("Product information extracted and saved to product_info.json")

