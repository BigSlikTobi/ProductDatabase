# ProductDatabase

Get product list by URL form (otto.de) commoncrawl.org, extracting the product urls from the list and getting the product descriptions and reviews for avery product into a DB.

How to: Only tested with otto.de

1. Collect product list information form commoncrawl.org with getProductURLs.py. This will create a product_record.json with available urls.
2. Get product links form the lists with getProductLink.py. This will create a product_info.json with product urls.
3. Create product database. Extract product name, product description from the products with createProductDatabase.py. Write the infos in a product_database.db
4. Get the reviews from the products available in the product database with getReviews.py. Write them in reviews.json 
5. Write the products in review json into the reviews database with createReviewDatabase.py 

