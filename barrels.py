# %%
import json
import os
import string
from datetime import datetime

def create_barrels():
    # File names
    lexicon_file = "Lexicon.json"
    inverted_index_file = "InverseIndexed.json"
    dataset_file = "Dataset.json"
    output_dir = "barrels"

    # Function to load JSON safely
    def load_json(file_name):
        with open(file_name, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading {file_name}: {e}")
                return None

    # Load Lexicon and InvertedIndex files
    lexicon = load_json(lexicon_file)
    inverted_index = load_json(inverted_index_file)

    # Load Dataset.json line by line
    dataset = []
    try:
        with open(dataset_file, 'r') as f:
            for line in f:
                try:
                    dataset.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding line in {dataset_file}: {e}")
    except FileNotFoundError:
        print(f"File {dataset_file} not found.")
        return

    if not lexicon or not inverted_index or not dataset:
        print("Failed to load one or more files. Ensure all JSON files are properly formatted.")
        return

    # Create a map from links to their dates
    link_date_map = {
        entry['link']: datetime.strptime(entry['date'], '%Y-%m-%d')
        for entry in dataset
    }

    # Initialize 27 barrels (a-z + # for non-alphabetic)
    barrels = {letter: {} for letter in string.ascii_lowercase + "#"}

    # Group words into barrels
    for word, word_id in lexicon.items():
        # Ensure the word is not empty before accessing its first letter
        if word:
            first_letter = word[0].lower() if word[0].isalpha() else "#"
        else:
            first_letter = "#"  # If the word is empty, categorize it as "#"
        
        if first_letter in barrels:
            # Get links from the inverted index and sort them by date
            links = inverted_index.get(str(word_id), [])
            sorted_links = sorted(links, key=lambda link: link_date_map.get(link, datetime.min), reverse=True)
            barrels[first_letter][word] = sorted_links

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Write barrels to JSON files
    for letter, words in barrels.items():
        output_file = os.path.join(output_dir, f"{letter}.json")
        with open(output_file, 'w') as f:
            json.dump(words, f, indent=4)

    print(f"Barrels created successfully in the '{output_dir}' directory.")

# Run the function
create_barrels()



