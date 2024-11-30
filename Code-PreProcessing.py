# %%
import pandas as pd




data = pd.read_json(r"C:/Users/shama/OneDrive/Desktop/Search Engine/NewsDataset.json", lines=True)


data_cleaned = data.drop_duplicates(subset=None, keep='first', inplace=False)

print(data_cleaned)


# %%
for column in data.columns:
    print(f"Unique values in '{column}': {data[column].unique()}")

# %%
print(f"Unique values in category are {data['category'].unique()}")



# %%
print(data.columns)

# %%
category_counts = data['category'].value_counts()


print(category_counts)

# %%
test = data.iloc[:20]
print(test.columns)

# %%



# %%
import nltk
nltk.download('averaged_perceptron_tagger_eng')

# %%
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, word_tokenize
import json

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize lemmatizer and stemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Define stop words, articles, and auxiliary verbs to remove
stop_words = set(stopwords.words('english'))
articles = {"a", "an", "the"}
auxiliary_verbs = {"may", "might", "could", "would", "shall", "should", "will", "can", "must"}

# Function to clean and process text (focus on nouns)
def process_text(text):
    if not text:  # Handle cases where text is empty or None
        return []
    
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    
    # POS tagging to extract only nouns (NN, NNS, NNP, NNPS)
    tagged_tokens = pos_tag(tokens)
    
    # Extract nouns based on POS tags
    nouns = [word for word, pos in tagged_tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
    
    # Remove articles and auxiliary verbs
    filtered_tokens = [word for word in nouns if word not in stop_words and word not in articles and word not in auxiliary_verbs]
    
    return filtered_tokens

# Function to clean links (remove embedded links, images, videos, and mp3s)
def clean_link(link):
    # Remove any links embedded within a link (URLs inside a URL)
    link = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "", link)
    
    # Remove images, videos, and mp3 file types
    link = re.sub(r"\.(jpg|jpeg|png|gif|mp4|avi|mov|mp3)$", "", link, flags=re.IGNORECASE)
    
    # Remove punctuation and special characters (keeping only alphanumeric and spaces)
    link = re.sub(r"[^\w\s]", "", link)
    
    return link

# Load the dataset from the JSON file
data = pd.read_json(r"C:/Users/shama/OneDrive/Desktop/Search Engine/NewsDataset.json", lines=True)


# Prepare data for JSON storage
processed_data = []

# Process each row in the dataset
for index, row in data.iterrows():
    # Clean and process the link
    clean_link_text = clean_link(row['link'])
    processed_link = process_text(clean_link_text)
    
    # Process other columns: headline, category, short description (same processing applied)
    processed_headline = process_text(row['headline'])
    processed_category = process_text(row['category'])
    processed_short_description = process_text(row['short_description'])
    
    # Combine all keywords into a single list and remove duplicates
    all_keywords = processed_link + processed_headline + processed_category + processed_short_description
    unique_keywords = list(set(all_keywords))  # Remove duplicates
    
    # Append processed data to the list
    processed_data.append({
        'link': row['link'],  # Original link
        'keywords': ", ".join(unique_keywords)  # Join keywords with a comma
    })

# Save processed data into a JSON file
output_file = 'C:/Users/shama/OneDrive/Desktop/Search Engine/Pre-ProcessedData.json'
with open(output_file, 'w') as f:
    json.dump(processed_data, f, indent=4)

print(f"Processed data has been saved to {output_file}")



