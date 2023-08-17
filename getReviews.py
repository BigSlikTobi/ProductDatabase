import sqlite3
import requests
from bs4 import BeautifulSoup
import json

def get_reviews(review_url):
    if review_url is None:
        print("Review URL is None. Skipping.")
        return []

    full_url = "https://otto.de" + review_url
    response = requests.get(full_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = []

        review_elements = soup.find_all('div', class_='cr_review')
        for review_element in review_elements:
            review_title = review_element.find('h4', class_='pl_headline50').text.strip()
            review_text = review_element.find('span', attrs={'data-qa': 'cr-review-text'}).text.strip()

            reviews.append({
                'product_id': None,  # Placeholder, to be filled later
                'product_name': None,  # Placeholder, to be filled later
                'review_title': review_title,
                'review_text': review_text
            })

        return reviews
    else:
        print(f"Failed to fetch reviews for URL: {full_url}")
        return []

def main():
    conn = sqlite3.connect('product_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, review_url FROM products WHERE hasReview = 0')
    products_to_update = cursor.fetchall()

    for product_id, product_name, review_url in products_to_update:
        reviews = get_reviews(review_url)

        for review in reviews:
            review['product_id'] = product_id
            review['product_name'] = product_name

        # Write the reviews to the JSON file (as separate arrays)
        with open('reviews.json', 'a', encoding='utf-8') as json_file:
            if json_file.tell() == 0:
                json_file.write("[")
            else:
                json_file.write(",")
            json.dump(reviews, json_file, indent=4, ensure_ascii=False)

        # Update the 'hasReview' field for the product
        cursor.execute("UPDATE products SET hasReview = 1 WHERE id = ?", (product_id,))
        conn.commit()

        print("Reviews written for:", product_name)

    with open('reviews.json', 'a', encoding='utf-8') as json_file:
        json_file.write("]")  # Close the array at the end

    conn.close()

if __name__ == '__main__':
    main()