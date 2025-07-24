import pandas as pd
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.stats import zscore
from sklearn.feature_extraction.text import TfidfVectorizer
from review_analysis.preprocessing.base_processor import BaseDataProcessor
import matplotlib
import nltk


class RottenTomatoesProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.df = None

    def preprocess(self):
        self.df = pd.read_csv(self.input_path)
        self.df.dropna(inplace=True)

        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce").dt.date
        self.df["rating"] = self.df["rating"] * 2
        self.df = self.df[(self.df["rating"] > 0) & (self.df["rating"] <= 10)]

        self.df["review_length"] = self.df["review"].apply(len)
        self.df["review_z"] = zscore(self.df["review_length"])
        self.df = self.df[self.df["review_z"] > -2]

        self.df["review"] = self.df["review"].apply(
            lambda x: re.sub("[^a-zA-Z0-9 ?]", "", x)
        )
        self.df["review"] = self.df["review"].apply(lambda x: word_tokenize(x))

        stop_words = set(stopwords.words("english"))
        self.df["review"] = self.df["review"].apply(
            lambda x: [w for w in x if w.lower() not in stop_words]
        )

        lemmatizer = WordNetLemmatizer()
        self.df["review"] = self.df["review"].apply(
            lambda x: [lemmatizer.lemmatize(w) for w in x]
        )
        self.df["review"] = self.df["review"].apply(lambda x: " ".join(x))

    def feature_engineering(self):
        vectorizer = TfidfVectorizer(max_features=100)
        tfidf_matrix = vectorizer.fit_transform(self.df["review"])
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out()
        )
        # TF-IDF 결과로 관련도 높은 키워드 추출
        self.df["keywords"] = tfidf_df.apply(
            lambda row: " ".join(
                row[row > 0].sort_values(ascending=False).head(5).index.tolist()
            ), axis=1
        )

    def save_to_database(self):
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        output_file = os.path.join(self.output_dir, f"preprocessed_{base_name}.csv")
        self.df.to_csv(output_file, index=False)

    def visualize(self):
        os.makedirs("review_analysis/plots", exist_ok=True)

        # ✅ 별점 히스토그램
        ratings = self.df["rating"]
        if isinstance(ratings, pd.DataFrame):
            ratings = ratings.iloc[:, 0]
        ratings = ratings.values

        if ratings.ndim != 1:
            print(f"[ERROR] rating shape 이상함: {ratings.shape}")
            return

        plt.figure(figsize=(8, 6))
        plt.hist(ratings, bins=10, edgecolor="black", color="steelblue")
        plt.title("Rating Distribution (RottenTomatoes)")
        plt.xlabel("Rating (out of 10)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("review_analysis/plots/rottentomatoes_rating_histogram.png")
        plt.close()

        # ✅ 단어 등장 빈도수 기준 Top 20
        review_series = self.df["review"].apply(str)
        all_text = " ".join(review_series).lower().strip()

        all_words = [
            w
            for w in all_text.split()
            if w.isalpha() and len(w) >= 3  # 숫자 제거, 최소 3자
        ]

        exclude_words = {"review", "movie", "film"}
        filtered_words = [w for w in all_words if w not in exclude_words]

        word_counts = Counter(filtered_words)
        common_words = word_counts.most_common(20)

        if not common_words:
            print("[WARN] 단어가 거의 없습니다. 리뷰 데이터 확인 필요.")
            return

        words, counts = zip(*common_words)
        plt.figure(figsize=(12, 6))
        plt.bar(words, counts)
        plt.xticks(rotation=45)
        plt.title("Top 20 Most Frequent Words in Reviews (Raw Frequency)")
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("review_analysis/plots/rottentomatoes_top20_frequent_words.png")
        plt.close()
