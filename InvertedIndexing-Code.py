import json

# File paths to your data
news_data_file = 'Pre-ProcessedData.json'
lexicon_file = 'lexicon.json'

# Function to load JSON data (e.g., from files)
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)  # This loads and returns the JSON data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return None

# Function to create a dictionary that maps word indices to URLs
def map_word_indices_to_urls(news_data, lexicon):
    # Initialize an empty dictionary to hold the final result
    word_index_to_urls = {}

    # Go through each document (news article)
    for document in news_data:
        url = document.get("link", "")  # Extract the URL of the document
        keywords = document.get("keywords", "").split(", ")  # Split the keywords into a list

        # Loop through each word in the keywords list
        for word in keywords:
            # Check if the word exists in the lexicon
            if word in lexicon:
                # Get the word index from the lexicon
                word_index = lexicon[word]

                # If the word index is not already in the dictionary, add it with an empty list
                if word_index not in word_index_to_urls:
                    word_index_to_urls[word_index] = []

                # Add the current URL to the list of URLs for this word index
                if url not in word_index_to_urls[word_index]:
                    word_index_to_urls[word_index].append(url)

    return word_index_to_urls  # Return the final dictionary

# Function to save the result to a new JSON file
def save_to_file(result, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)  # Save the dictionary to a JSON file with indentation

# Main function to load data, map indices to URLs, and save the result
def main():
    # Load the news data and lexicon
    news_data = load_data(news_data_file)
    lexicon = load_data(lexicon_file)

    if news_data and lexicon:  # Proceed only if data is successfully loaded
        # Generate the dictionary that maps word indices to URLs
        word_index_to_urls = map_word_indices_to_urls(news_data, lexicon)

        # Specify the output file where we'll save the result
        output_file = 'InverseIndexed.json'

        # Save the result to a file
        save_to_file(word_index_to_urls, output_file)

        print("Word indices to URLs mapping has been successfully generated and saved!")
    else:
        print("Failed to load data. Please check your JSON files.")

# Run the main function to start the process
if __name__ == '__main__':
    main()
