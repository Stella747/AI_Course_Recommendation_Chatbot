# 🎓 AI Course Recommendation Chatbot

## 🚀 Overview

This project is an AI-powered chatbot that recommends online courses based on user interests using Natural Language Processing (NLP).

## 💡 Problem

With thousands of online courses available, users often struggle to find relevant content aligned with their interests.

## ✅ Solution

This chatbot takes user input (e.g., "I want to learn data science") and recommends the most relevant courses using a content-based filtering approach.

## 🧠 Tech Stack

* Python
* Pandas
* Scikit-learn (TF-IDF, Cosine Similarity)
* Streamlit (UI)

## ⚙️ How it Works

1. Course dataset is processed and combined into a single text feature
2. TF-IDF vectorization is applied
3. User input is converted into vector form
4. Cosine similarity is used to find the most relevant courses

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Example

**Input:**
"I want to learn AI"

**Output:**

* Artificial Intelligence - Learning & Theory
* What is Data Science?
* Machine Learning Basics

## 📌 Future Improvements

* Use LLM (OpenAI / HuggingFace)
* Add user personalization
* Deploy on cloud (Streamlit Cloud / AWS)

## 👩‍💻 Author

Renu Meena
