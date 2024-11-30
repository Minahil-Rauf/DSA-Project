import json

# Load the preprocessed data from the file
with open('Pre-ProcessedData.json', 'r') as file:
    data = json.load(file)

# Initialize an empty set to store unique words
unique_words = set()

# Extract keywords from each article and add them to the set
for article in data:
    keywords = article["keywords"].split(", ")
    unique_words.update(keywords)

# Create a lexicon by mapping each unique word to a unique index
lexicon = {word: idx for idx, word in enumerate(sorted(unique_words))}

# Save the lexicon as a JSON file
with open('lexicon.json', 'w') as f:
    json.dump(lexicon, f, indent=4)

# Output the lexicon (optional, for debugging)
print(json.dumps(lexicon, indent=4))
