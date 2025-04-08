import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample dataset for training the vectorizer
texts = [
    "I am happy", 
    "I feel sad", 
    "I am angry", 
    "Feeling relaxed and peaceful",
    "I am excited today", 
    "I am very frustrated", 
    "Feeling neutral"
]

# Train a TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(texts)

# Save the vectorizer
with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

print("✅ Vectorizer saved successfully!")
