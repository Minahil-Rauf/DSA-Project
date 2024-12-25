from flask import Flask, render_template, request, jsonify
import nltk
import json
import os
import requests
from bs4 import BeautifulSoup
import re
import time

# Download necessary nltk resources
nltk.download('punkt')

# Path to barrels directory
barrels_dir = 'barrels'

app = Flask(__name__)

def search_in_barrels(query):
    results = []
    if len(query) > 3:
        barrel_file = os.path.join(barrels_dir, f"{query[0]}.json")
    if os.path.exists(barrel_file):
        with open(barrel_file, 'r') as f:
            data = json.load(f)
            
            # Navigate through the data structure
            if query[0] in data and query[1] in data[query[0]] and query[2] in data[query[0]][query[1]]:
                results = data[query[0]][query[1]][query[2]]

                # Extract exact matches
                exact_results = []
                if isinstance(results, list):  # If results is a list
                    for item in results:
                        if isinstance(item, list) and len(item) > 0 and item[0] == query:
                            exact_results.append(item)
                results = exact_results  # Update results to contain only exact matches
                    
    # Case 1: Query is 1 letter (search entire barrel)
    elif len(query) == 1:
        barrel_file = os.path.join(barrels_dir, f"{query[0]}.json")

        # If the barrel file exists, search through it
        if os.path.exists(barrel_file):
            with open(barrel_file, 'r') as f:
                data = json.load(f)

                # Check if the first letter exists in the barrel
                if query[0] in data:
                    for second_level_key in data[query[0]].values():
                        for third_level_key in second_level_key.values():
                            results.extend(third_level_key)  # Add all words from all sub-bins

    # Case 2: Query is 2 letters (search second-level bins)
    elif len(query) == 2:
        barrel_file = os.path.join(barrels_dir, f"{query[0]}.json")

        # If the barrel file exists, search through it
        if os.path.exists(barrel_file):
            with open(barrel_file, 'r') as f:
                data = json.load(f)

                # Check if the first letter exists in the barrel and the second level exists
                if query[0] in data and query[1] in data.get(query[0], {}):
                    for second_level_key, second_level_value in data[query[0]][query[1]].items():
                        results.extend(second_level_value)  # Add results from each bin inside

    # Case 3: Query is 3 letters (search third-level bins)
    elif len(query) == 3:
        barrel_file = os.path.join(barrels_dir, f"{query[0]}.json")

        # If the barrel file exists, search through it
        if os.path.exists(barrel_file):
            with open(barrel_file, 'r') as f:
                data = json.load(f)

                # Check if the query exists in the third-level bins
                if query[0] in data and query[1] in data[query[0]] and query[2] in data[query[0]][query[1]]:
                    results = data[query[0]][query[1]][query[2]]
                
                    
    return results

def convert_to_comma_separated_urls(data):
    urls = [url for _, url_list in data for url in url_list]
    return ", ".join(urls)

def normalize_word(word):
    word = word.lower()
    if word.endswith('s'):
        word = word[:-1]
    return word

def save_urls_to_json(urls, filename, query_words):
    try:
        url_list = [url.strip() for url in urls.split(',') if url.strip()]
        if not url_list:
            return "No valid URLs provided."
        
        url_list = url_list[:10]
        page_data = []
        normalized_query_words = {normalize_word(word) for word in query_words}

        for url in url_list:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else "No Title"
                    description = ""
                    meta_description = soup.find('meta', attrs={'name': 'description'})
                    if meta_description and meta_description.get('content'):
                        description = meta_description['content']
                    else:
                        page_text = soup.get_text(strip=True)
                        page_text = re.sub(r'[^\w\s]', '', page_text)
                        description = ' '.join(page_text.split()[:50])

                    keywords = description.split()[:5]
                    relevance_score = 0
                    
                    for keyword in keywords:
                        normalized_keyword = normalize_word(keyword)
                        if normalized_keyword in normalized_query_words:
                            relevance_score += 5

                    page_data.append({
                        "url": url,
                        "title": title,
                        "description": description,
                        "keywords": keywords,
                        "relevance_score": relevance_score,
                        "query_words": query_words
                    })
                else:
                    print(f"Failed to fetch the URL {url}. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching the URL {url}: {e}")

        page_data_sorted = sorted(page_data, key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"Page Data Sorted: {page_data_sorted}")

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(page_data_sorted, json_file, indent=4, ensure_ascii=False)
            print(f"Data saved to {filename}")

        return page_data_sorted
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return "No search query provided"
    
    start_time = time.time()

    words = nltk.word_tokenize(query)
    words = [word.lower() for word in words]
    
    results = []
    for word in words:
        results.extend(search_in_barrels(word))

    if not results:
        return "No results found"
    else:
        urls = convert_to_comma_separated_urls(results)
        filename = 'results.json'
        sorted_data = save_urls_to_json(urls, filename, words)
        
        end_time = time.time()
        search_duration = end_time - start_time
        
        print(f"Search completed in {search_duration:.2f} seconds.")

        return render_template('NewsLinker.html', results=sorted_data, search_duration=search_duration)

if __name__ == '__main__':
    app.run(debug=True)