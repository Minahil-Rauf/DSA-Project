# %%
import json
from datetime import datetime

# File paths
news_data_file = 'Dataset.json'
lexicon_file = 'Lexicon.json'
preprocessed_file = 'Pre-ProcessedData.json'
output_file = 'InverseIndexed.json'

# Function to load line-delimited JSON (Dataset.json)
def load_line_delimited_json(file_name):
    dataset = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    dataset.append(json.loads(line.strip()))
                except json.JSONDecodeError as e:
                    print(f"Error decoding line in {file_name}: {e}")
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    return dataset

# Function to load regular JSON (Lexicon.json and Pre-ProcessedData.json)
def load_json(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading {file_name}: {e}")
        return None

# Function to calculate the page rank value for a document
def calculate_page_rank(document, word):
    headline = document.get("headline", "")
    short_description = document.get("short_description", "")
    date_str = document.get("date", "")

    # Calculate word weights based on presence in fields
    word_count = 0
    word_count += headline.split().count(word) * 5
    word_count += short_description.split().count(word) * 3

    # Add date factor
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        days_ago = (datetime.now() - date).days
        date_weight = max(5 - days_ago / 30, 0)  # Recent links prioritized, decays over time
    except ValueError:
        date_weight = 0  # If date is invalid or missing

    return word_count + date_weight

# Quick sort function for sorting URLs by page rank
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[1] > pivot[1]]
    middle = [x for x in arr if x[1] == pivot[1]]
    right = [x for x in arr if x[1] < pivot[1]]
    return quick_sort(left) + middle + quick_sort(right)

# Function to map word indices to ranked URLs (backward indexing)
def map_word_indices_to_urls(news_data, lexicon, links):
    word_index_to_urls = {}

    for word, word_index in lexicon.items():
        links_with_word = []

        for link in links:
            document = next((doc for doc in news_data if doc["link"] == link), None)
            if document:
                page_rank = calculate_page_rank(document, word)
                links_with_word.append((link, page_rank))

        # Sort the links based on page rank in descending order
        links_with_word = quick_sort(links_with_word)
        word_index_to_urls[word_index] = [url for url, rank in links_with_word]

    return word_index_to_urls

# Main function
def main():
    # Load data
    news_data = load_line_delimited_json(news_data_file)
    lexicon = load_json(lexicon_file)
    preprocessed_data = load_json(preprocessed_file)

    if not (news_data and lexicon and preprocessed_data):
        print("Failed to load necessary data files.")
        return

    # Extract the first 5 links
    first_five_links = [entry["link"] for entry in preprocessed_data[:5]]

    # Generate the inverted index
    inverted_index = map_word_indices_to_urls(news_data, lexicon, first_five_links)

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, indent=4)

    print(f"Inverted index has been successfully generated and saved to {output_file}.")

if __name__ == '__main__':
    main()



