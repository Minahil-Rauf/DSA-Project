# Search Engine

This project consists of several Python scripts that preprocess text data, perform forward indexing, and generate inverted indexes. It also includes various JSON files for efficient text retrieval and indexing, as well as a barrels.py script for barrel-related processing.

## Files Included:

- **Code-PreProcessing.py**: Preprocesses the input text data by performing necessary steps like tokenization, removing stopwords, and stemming/lemmatization.
  
- **ForwardIndexingCode.py**: Generates a forward index from the preprocessed data.

- **InvertedIndexing-Code.py**: Creates an inverted index, which maps terms to the documents in which they appear.

- **files.json**: Contains all JSON files, including:
  - **lexicon.json**: Lexicon with terms and their corresponding document occurrences.
  - **forward_index.json**: Forward index data.
  - **backward_index.json**: Inverted index data.
  - **barrels.json**: Barrel-related data for efficient text retrieval.
  - **dataset.json**: The dataset used for indexing.
  - **preprocessing.json**: Data resulting from the preprocessing steps.
  
- **LexiconCode.py**: Handles the creation and management of the lexicon file used for indexing and retrieval.

- **barrels.py**: Contains code for barrel-related processing and management of barrel data.

## Installation

To run the scripts, you will need to install the following Python libraries:

- **nltk**: For natural language processing tasks like tokenization, stopword removal, etc.
- **pandas**: For data manipulation and storage.

## Usage
- First, run **Code-PreProcessing.py** to preprocess the text data.
- Next, execute **ForwardIndexingCode.py** to generate the forward index.
- Then, run **InvertedIndexing-Code.py** to create the inverted index.
- The **files.json** file will be generated automatically, storing all the JSON data used in the indexing process.
- Use **LexiconCode.py** to interact with or manage the lexicon as needed.
- Use **barrels.py** for barrel-related processing.

You can access and download the **files.json** file, which includes all the JSON files, from the following link:  
https://drive.google.com/file/d/1AE_VgejbzJDNws0sUUwmL0nUxKIgSu2a/view?usp=drive_link
