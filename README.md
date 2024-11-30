This project consists of several Python scripts that preprocess text data, perform forward indexing, and generate inverted indexes. It also includes a lexicon for efficient text retrieval.

*Files Included*:
Code-PreProcessing.py: Preprocesses the input text data by performing necessary steps like tokenization, removing stopwords, and stemming/lemmatization.

ForwardIndexingCode.py: Generates a forward index from the preprocessed data.

InvertedIndexing-Code.py: Creates an inverted index, which maps terms to the documents in which they appear.

Lexicon.json: Contains a lexicon with terms and their corresponding document occurrences, used in the indexing process.

LexiconCode.py: Handles the creation and management of the lexicon file used for indexing and retrieval.

*Installation*:
To run the scripts, you will need to install the following Python libraries:

nltk: For natural language processing tasks like tokenization, stopword removal, etc.
pandas: For data manipulation and storage.
You can install these dependencies by running the following command:

bash
*Copy code*
pip install nltk pandas
*Usage*:
First, run Code-PreProcessing.py to preprocess the text data.
Next, execute ForwardIndexingCode.py to generate the forward index.
Then, run InvertedIndexing-Code.py to create the inverted index.
The Lexicon.json file will be generated automatically, storing the lexicon used in the indexing process.
Use LexiconCode.py to interact with or manage the lexicon as needed.
