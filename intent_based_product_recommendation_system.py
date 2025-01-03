# -*- coding: utf-8 -*-
"""Intent-Based Product Recommendation System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dsrrRQy6VK9tCRd4AhfK8nji5REbQg6X
"""

!pip install pandas numpy matplotlib seaborn sentence-transformers scikit-learn tqdm nltk transformers

# these are the libraries are needed to import for data processing, data manipulation, numerical analysis, tranformation of data into different type and shapes
# if there comes any issue regarding importing libraries check the dependancies, version and either specific library is install or not
# before use of any library it is recommended to study documentation where developer can understand the meaning and use of library for his/her purpose
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
from transformers import AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, confusion_matrix
from tqdm import tqdm

# step 2: text data preprocessing using nltk(natural language toolkit, a NLP library)
# this step will trim the unncessary data e.g. words, punctuation marks, phrases etc
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# load or get data using local command or inbuild functions
path = "/content/home appliance skus lowes.csv"
# for beginners you can take this step df = pd.read_csv('/content/home appliance skus lowes.csv')
# but i already took path = '/content/home appliance skus lowes.csv' so instead of using link i pasted path
df = pd.read_csv(path)

df.shape

df.info()

df.describe()

df.isnull().sum()

# Convert all columns with string data to lowercase
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Columns to drop
columns_to_drop = ['DATE_SCRAPED', 'RUN_START_DATE', 'SHIPPING_LOCATION', 'SKU',
                   'PRODUCT_URL', 'BESTSELLER_RANK', 'COUNTRY', 'SELLER']
df = df.drop(columns=columns_to_drop, errors = 'ignore')

df['PROMOTION'] = df['PROMOTION'].fillna('Not Promotion')

# apply pre-trained model from transformer hugging face all-MiniLM-L6-v2
model = SentenceTransformer('all-MiniLM-L6-v2')

# generate embeddings for PRODUCT_NAME column in batches for better performance
def generate_embeddings_in_batches(df, batch_size = 32):
  embeddings = []
  for i in tqdm(range(0, len(df), batch_size)):
    batch = df.iloc[i:i+batch_size]
    embeddings_batch = model.encode(batch['PRODUCT_NAME'].tolist(), batch_size=batch_size)
    embeddings.extend(embeddings_batch)
  return embeddings

# Compute and store embeddings for all product names
print("Generating embeddings for products and catagories...")
df['product_name_embedding'] = generate_embeddings_in_batches(df)

# Ensure that the CATEGORY column is lowercase and free of extra spaces
df['CATEGORY'] = df['CATEGORY'].str.lower().str.strip()

# Define a function to find the best matching product
def find_best_match(query, df):
    """Match query to the most relevant product based on embeddings and intent."""
    # Detect intent using zero-shot classification
    intent = classify_intent(query)
    print(f"Detected Intent: {intent}")

    # Filter products based on detected intent
    # Ensure CATEGORY is consistently formatted and match against the intent
    df_filtered = df[df['CATEGORY'].str.contains(intent.lower(), case=False, na=False)]

    if df_filtered.empty:
        return {"Error": f"No products found for the intent: {intent}"}

    # Generate query embedding
    query_embedding = model.encode(query)

    # Calculate cosine similarity with the filtered product embeddings
    similarities = cosine_similarity([query_embedding], df_filtered['product_name_embedding'].tolist())
    best_match_idx = similarities.argmax()
    best_match = df_filtered.iloc[best_match_idx]

    return best_match

# Example query
query = "I need a product to cook food "

# Find the best match
best_match = find_best_match(query, df)

# Display results
if "Error" in best_match:
    print(best_match["Error"])
else:
    print("Best Match:")
    print(f"Product Name: {best_match['PRODUCT_NAME']}")
    print(f"Brand: {best_match['BRAND']}")
    print(f"Price: {best_match['PRICE_RETAIL']} {best_match['CURRENCY']}")
    print(f"Product URL: {best_match['WEBSITE_URL']}")

"""**Intent-Based Product Recommendation System**

Overview:
This project is an intent-based product recommendation system that matches user queries to the most relevant product from a dataset. The model utilizes natural language processing (NLP) techniques, pre-trained embeddings, and intent classification to achieve this.

The project aims to serve as an example of leveraging pre-trained models and open-source NLP tools to build intelligent recommendation systems.
Dependencies
The following libraries are required to run this project:

Python Libraries
Core Libraries:

numpy: For numerical computations.
pandas: For data manipulation and preprocessing.

Natural Language Processing:

nltk: For text preprocessing tasks such as tokenization, stopword removal, and lemmatization.
Submodules used:
punkt (tokenization)
wordnet (lemmatization)
stopwords (removal of common words)
transformers: For using pre-trained models and pipelines from Hugging Face.
sentence-transformers: To compute embeddings of textual data using pre-trained sentence-level models.
tqdm: For creating progress bars during large computations.
Machine Learning:

scikit-learn: For evaluation metrics (e.g., accuracy, confusion matrix) and similarity computation.
Data Requirements
Input Data:
A CSV file containing product details, including the following key columns:
CATEGORY: The high-level category (e.g., "electronics", "furniture").
PRODUCT_NAME: The name or description of the product.
Other columns such as BRAND, PRICE_RETAIL, CURRENCY, and WEBSITE_URL for contextual details.
Pre-trained Model:
Sentence Transformer Model: all-MiniLM-L6-v2 (from Hugging Face) is used to compute sentence embeddings for the product names.
How It Works
Data Preprocessing:

Convert all text to lowercase for consistency.
Drop unnecessary columns to streamline the dataset.
Fill missing values in specific columns (e.g., PROMOTION) with default values.
Embedding Generation:

Use all-MiniLM-L6-v2 to compute sentence embeddings for product names. These embeddings represent the semantic meaning of the text.
Intent Detection:

Use Hugging Face's zero-shot classification pipeline to detect the user's intent from their query.
Match the detected intent to the appropriate product category.
Product Matching:

Compute cosine similarity between the query's embedding and product embeddings within the relevant category.
Recommend the product with the highest similarity score.
Evaluation:

Test the system with predefined queries.
Compute accuracy and visualize the confusion matrix to understand performance.
"""