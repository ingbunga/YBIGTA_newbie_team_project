import pandas as pd
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.stats import zscore
from sklearn.feature_extraction.text import TfidfVectorizer
from review_analysis.preprocessing.base_processor import BaseDataProcessor
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

class LetterboxdProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.df = None  # 데이터를 담을 속성

    def preprocess(self):
        # CSV 파일 불러오기
        self.df = pd.read_csv(self.input_path)

        # 결측치 제거
        self.df.dropna(inplace=True)

        # 날짜 포맷 변환
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce').dt.date
        
        # rating 10점으로 통일
        self.df['rating'] = self.df['rating']*2
        self.df = self.df[(self.df['rating'] > 0) & (self.df['rating'] <= 10)]
        
        #너무 짧은 리뷰 제거
        self.df['review_length'] = self.df['review'].apply(len)
        self.df['review_z'] = zscore(self.df['review_length'])
        self.df = self.df[self.df['review_z'] > -2]

        #특수문자 제거, 토큰화, 불용어 제거, 표제어 추출
        self.df['review'] = self.df['review'].apply(lambda x: re.sub('[^a-zA-Z0-9 ?]', '', x))
        self.df['review'] = self.df['review'].apply(lambda x: word_tokenize(x))

        stop_words = set(stopwords.words('english'))
        self.df['review'] = self.df['review'].apply(lambda x: [word for word in x if word not in stop_words])

        lemmatizer = WordNetLemmatizer()
        self.df['review'] = self.df['review'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

        #TF-IDF를 위해 다시 문자열로 변환
        self.df['review'] = self.df['review'].apply(lambda x: ' '.join(x))

    def feature_engineering(self):
        #TF-IDF로 벡터화
        vectorizer = TfidfVectorizer(max_features=10000)
        tfidf_matrix = vectorizer.fit_transform(self.df['review'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
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
        plt.figure(figsize=(8, 6))
        counts = self.df['rating'].iloc[:,0].value_counts().sort_index()

        # 컬러 맵으로 색상 강도 조절
        colors = sns.color_palette("Blues", n_colors=len(counts))
        
        plt.bar(counts.index, counts.values, color=colors)

        plt.title("Rating Distribution (Letterboxd)", fontsize=14)
        plt.xlabel("Rating (out of 10)")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig("review_analysis/plots/letterboxd_rating_histogram.png")
        plt.show()

        exclude_words = {"review", "movie", "film"}
        tokenized = self.df['review'].iloc[:,0].apply(lambda x: word_tokenize(x))
        tokenized = tokenized.apply(lambda review: [word for word in review if len(word) >= 3 and word.isalpha() if word not in exclude_words])

        word_counts = Counter([word for review in tokenized for word in review])
        common_words = word_counts.most_common(20)

        words, freqs = zip(*common_words)
        colors = sns.color_palette("Blues_r", n_colors=20)

        plt.figure(figsize=(12, 6))
        sns.barplot(x=list(words), y=list(freqs), palette=colors)

        plt.title(f"Top {20} Most Frequent Words in Reviews (Letterboxd)", fontsize=14)
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig("review_analysis/plots/letterboxd_top20_frequent_words.png")
        plt.show()
