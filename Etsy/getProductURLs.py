import requests
import argparse
import json

# Parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--domain", required=True, help="The domain to target, e.g., amazon.de")
ap.add_argument("-i", "--index_list", nargs="+", default=["2022-49", "2022-40", "2022-33", "2022-27", "2022-21"],
                help="List of index versions to search (default: 2022-49 2022-40 2022-33 2022-27 2022-21)")
ap.add_argument("-m", "--max_hits", type=int, default=100, help="Maximum number of hits to retrieve (default: 100)")
args = vars(ap.parse_args())

domain = args['domain']
index_list = args['index_list']
max_hits = args['max_hits']
search_string = ""  # Change this variable to the desired string

def search_domain(domain, index_list, max_hits=100):
    record_list = []
    print("[*] Trying target domain: %s" % domain)

    for index in index_list:
        print("[*] Trying index %s" % index)
        cc_url = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain

        response = requests.get(cc_url)

        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_data = json.loads(record)
                if record_data['status'] == '200' and search_string in record_data['url']:
                    record_list.append(record_data)
                    if len(record_list) >= max_hits:
                        break  # Stop once the maximum number of hits is reached
            print("[*] Added %d results." % len(records))
            if len(record_list) >= max_hits:
                break  # Stop once the maximum number of hits is reached
    print("[*] Found a total of %d hits." % len(record_list))

    return record_list

def main():
    print("Starting CommonCrawl Search")
    record_list = search_domain(domain, index_list, max_hits)

    with open('product_records.json', 'w') as json_file:
        json.dump(record_list, json_file, indent=4)
        print("Common Crawl records with status code 200 and '%s' in the URL saved to product_records.json" % search_string)

if __name__ == '__main__':
    main()
