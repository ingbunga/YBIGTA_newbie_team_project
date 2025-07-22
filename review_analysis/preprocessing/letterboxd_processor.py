import pandas as pd
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.stats import zscore
from sklearn.feature_extraction.text import TfidfVectorizer
from review_analysis.preprocessing.base_processor import BaseDataProcessor

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
        self.df = pd.concat([self.df.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)

    def save_to_database(self):
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        dir_path = os.path.dirname(self.input_path) 
        output_file = os.path.join(dir_path, f"preprocessed_reviews_{base_name}.csv")
        self.df.to_csv(output_file, index=False)
