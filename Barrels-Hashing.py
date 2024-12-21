# %%
import json
import os
import string

def create_barrels():
    # File name for the inverted index
    inverted_index_file = "InverseIndexed.json"
    output_dir = "barrels"

    # Function to load JSON safely
    def load_json(file_name):
        with open(file_name, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading {file_name}: {e}")
                return None

    # Load the InvertedIndex file
    inverted_index = load_json(inverted_index_file)

    if not inverted_index:
        print("Failed to load InvertedIndex.json. Ensure it is properly formatted.")
        return

    # Initialize 26 barrels (a-z)
    barrels = {letter: {} for letter in string.ascii_lowercase}

    # Process words in InvertedIndex and group them into barrels
    for word, links in inverted_index.items():
        if not links:  # Skip words with no links
            continue
        
        # Ensure the word is not empty before accessing its first letter
        if word:
            first_letter = word[0].lower() if word[0].isalpha() else "#"
        else:
            first_letter = "#"  # If the word is empty, categorize it as "#"

        if first_letter in barrels:
            barrels[first_letter][word] = links

    # Create hash tables for each barrel
    for barrel_letter, words in barrels.items():
        # Initialize hash table for each barrel
        hash_table = {char1: {char2: {char3: [] for char3 in string.ascii_lowercase} for char2 in string.ascii_lowercase} for char1 in string.ascii_lowercase}

        # Fill hash table with words
        for word, links in words.items():
            # Ensure each level of hash table exists before appending
            char1 = word[0]
            if char1 not in hash_table:
                hash_table[char1] = {}
            
            if len(word) >= 2:
                char2 = word[1]
                if char2 not in hash_table[char1]:
                    hash_table[char1][char2] = {}
                
                if len(word) >= 3:
                    char3 = word[2]
                    if char3 not in hash_table[char1][char2]:
                        hash_table[char1][char2][char3] = []
                    hash_table[char1][char2][char3].append((word, links))
                else:
                    # For 2-character words, use "#" for third character
                    if "#" not in hash_table[char1][char2]:
                        hash_table[char1][char2]["#"] = []
                    hash_table[char1][char2]["#"].append((word, links))
            else:
                # For 1-character words, use "#" for second and third characters
                if "#" not in hash_table[char1]:
                    hash_table[char1]["#"] = {}
                if "#" not in hash_table[char1]["#"]:
                    hash_table[char1]["#"]["#"] = []
                hash_table[char1]["#"]["#"].append((word, links))

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Write barrels with hash tables to JSON files
        output_file = os.path.join(output_dir, f"{barrel_letter}.json")
        with open(output_file, 'w') as f:
            json.dump(hash_table, f, indent=4)

    print(f"Barrels with hash tables created successfully in the '{output_dir}' directory.")

# Run the function
create_barrels()



