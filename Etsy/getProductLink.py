import requests
import json
from bs4 import BeautifulSoup

def extract_product_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_info = []
        
        product_elements = soup.find_all('a', class_='listing-link wt-display-inline-block')
        for product_element in product_elements:
            product_link = product_element.get('data-palette-listing-image') or product_element.get('href')
            brand_name = product_element.get('title')
            
            if product_link and brand_name:
                product_info.append({
                    'href': product_link,
                    'brand_name': brand_name
                })
            else:
                img_element = product_element.find('img', class_='wt-width-full wt-height-full wt-display-block')
                if img_element:
                    product_link = img_element.get('data-listing-card-listing-image')
                    brand_name = img_element.get('alt')
                    
                    if product_link and brand_name:
                        product_info.append({
                            'href': product_link,
                            'brand_name': brand_name
                        })
                    else:
                        print("Skipping URL:", url, "- Missing product link or brand name")
                else:
                    print("Skipping URL:", url, "- Missing product link or brand name")
            
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
