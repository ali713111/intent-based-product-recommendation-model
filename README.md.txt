# Intent-Based Product Recommendation System

## Overview
This project is an intent-based product recommendation system that matches user queries to the most relevant product from a dataset. The model utilizes natural language processing (NLP) techniques, pre-trained embeddings, and intent classification to achieve this.

## Dependencies
The following libraries are required to run this project:
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `nltk`
- `transformers`
- `sentence-transformers`
- `scikit-learn`
- `tqdm`

## Data Requirements
- **Input Data**: A CSV file containing product details, with key columns like:
  - `CATEGORY`: The high-level category (e.g., "electronics", "furniture").
  - `PRODUCT_NAME`: The name or description of the product.

- **Pre-trained Model**: `all-MiniLM-L6-v2` (from Hugging Face) for sentence embeddings.

## How It Works
1. **Data Preprocessing**:
   - Converts all text to lowercase.
   - Drops unnecessary columns.
   - Fills missing values.

2. **Embedding Generation**:
   - Computes sentence embeddings for product names.

3. **Intent Detection**:
   - Uses Hugging Face's zero-shot classification to detect user intent.

4. **Product Matching**:
   - Matches user queries with products based on cosine similarity of embeddings.

5. **Evaluation**:
   - Tests the system with predefined queries.
   - Computes accuracy and confusion matrix for performance.

## Usage
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

