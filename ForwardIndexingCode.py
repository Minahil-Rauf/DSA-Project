import json
import re

# Function to sanitize keywords (remove unwanted characters and spaces)
def sanitize_keyword(keyword):
    # Remove leading/trailing spaces, and any unwanted characters like % and quotes
    keyword = keyword.strip()
    keyword = re.sub(r"[^a-zA-Z0-9]+", "", keyword)  # Removes non-alphanumeric characters
    return keyword

# Load the preprocessed data from the file
with open('Pre-ProcessedData.json', 'r') as file:
    data = json.load(file)

# Load the lexicon from the file (lexicon format: {word: index})
with open('lexicon.json', 'r') as lexicon_file:
    lexicon = json.load(lexicon_file)

# Initialize a dictionary to store the forward index
forward_index = {}

# Reverse the lexicon to get word -> index mapping
word_to_index = {word: index for word, index in lexicon.items()}

# Process each article and create forward index
for article in data:
    link = article.get("link")
    keywords = article.get("keywords", "").split(", ")  # Get keywords or empty string if missing
    
    # Sanitize and map the keywords to their lexicon indexes
    word_indexes = [word_to_index.get(sanitize_keyword(keyword), None) for keyword in keywords]
    # Remove None values (words not found in lexicon)
    word_indexes = [index for index in word_indexes if index is not None]
    
    # Add to the forward index: map the link to its list of word indexes
    forward_index[link] = word_indexes

# Save the forward index as a JSON file
with open('Forward.json', 'w') as f:
    json.dump(forward_index, f, indent=4)

# Output the forward index (optional, for debugging)
print(json.dumps(forward_index, indent=4))
