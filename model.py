"""Content-based course recommendations using TF-IDF and cosine similarity."""

from functools import lru_cache
from pathlib import Path
import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = Path(__file__).parent / "data" / "courses.json"


@lru_cache(maxsize=1)
def _load_catalog():
    """Load and vectorize the bundled catalog once per app process."""
    with DATA_PATH.open(encoding="utf-8") as catalog_file:
        records = json.load(catalog_file)

    courses = pd.DataFrame(records)
    required_columns = {"name", "description"}
    if not required_columns.issubset(courses.columns):
        raise ValueError("Course catalog must include name and description fields.")

    courses = courses.dropna(subset=["name", "description"]).copy()
    courses["name"] = courses["name"].astype(str).str.strip()
    courses["description"] = courses["description"].astype(str).str.strip()
    courses = courses[(courses["name"] != "") & (courses["description"] != "")]
    courses = courses.drop_duplicates(subset=["name", "description"]).reset_index(drop=True)
    courses["content"] = courses["name"] + " " + courses["description"]

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    course_vectors = vectorizer.fit_transform(courses["content"])
    return courses, vectorizer, course_vectors


def recommend_courses(query, top_n=5):
    """Return the most relevant courses for a free-text learning goal.

    Results include a 0–1 cosine-similarity score. Courses with no lexical
    overlap are omitted so unrelated recommendations are not presented as matches.
    """
    query = " ".join(str(query or "").split())
    if not query:
        return pd.DataFrame(columns=["name", "description", "slug", "score"])
    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    courses, vectorizer, course_vectors = _load_catalog()
    query_vector = vectorizer.transform([query])
    if query_vector.nnz == 0:
        return pd.DataFrame(columns=["name", "description", "slug", "score"])

    scores = cosine_similarity(query_vector, course_vectors).ravel()
    matching_indices = scores.argsort()[::-1]
    matching_indices = [index for index in matching_indices if scores[index] > 0][:top_n]
    if not matching_indices:
        return pd.DataFrame(columns=["name", "description", "slug", "score"])

    results = courses.iloc[matching_indices].copy()
    results["score"] = scores[matching_indices]
    if "slug" not in results:
        results["slug"] = ""
    return results[["name", "description", "slug", "score"]].reset_index(drop=True)
