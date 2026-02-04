import re
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text: str, top_n: int = 20) -> list:
    text = clean_text(text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=top_n
    )

    tfidf_matrix = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()
