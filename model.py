import pandas as pd
import neattext.functions as nfx
import joblib
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data
nltk.download('wordnet')

# Load dataset
df = pd.read_csv("emotion_dataset_raw.csv")

# Handle missing values
df.dropna(subset=['Text', 'Emotion'], inplace=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Text preprocessing function
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = nfx.remove_userhandles(text)  # Remove @username
    text = nfx.remove_stopwords(text)  # Remove stopwords
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])  # Lemmatization
    return text

# Apply preprocessing
df['Clean_Text'] = df['Text'].apply(clean_text)

# Features and labels
X = df['Clean_Text']
y = df['Emotion']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Define pipeline with TF-IDF and SVM
pipe_svm = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ('svm', SVC(kernel='linear', C=1.0, probability=True))
])

# Train model (⚡ Faster, No GridSearchCV)
pipe_svm.fit(X_train, y_train)

# Predict
y_pred = pipe_svm.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print("🔹 Accuracy:", accuracy)
print("🔹 Classification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=df['Emotion'].unique(), yticklabels=df['Emotion'].unique())
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

# Save optimized model
joblib.dump(pipe_svm, "fast_text_emotion_svm.pkl")
print("✅ Fast model saved successfully!")
