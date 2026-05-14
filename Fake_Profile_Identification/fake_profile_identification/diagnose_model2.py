import pandas as pd
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

path = 'Profile_Datasets.csv'
df = pd.read_csv(path).fillna('')
print('rows', len(df))
print('label_counts:', df['Label'].value_counts().to_dict())

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'"@', '', text)
    text = re.sub(r'@', '', text)
    text = re.sub(r'https://', '', text)
    return ' '.join(text.split())

def build_feature_text(row):
    parts = [
        clean_text(row['name']),
        clean_text(row['screen_name']),
        clean_text(row['description']),
        clean_text(row['created_at']),
        clean_text(row['location']),
        clean_text(row['default_profile']),
    ]
    for field in ['statuses_count', 'followers_count', 'friends_count']:
        val = row[field]
        if val not in ('', None):
            parts.append(str(val).strip())
    return ' '.join(parts)

df['text_features'] = df.apply(build_feature_text, axis=1)
vectorizer = CountVectorizer(lowercase=True)
X = vectorizer.fit_transform(df['text_features'])
y = df['Label'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
models = [('svm', svm.LinearSVC(max_iter=10000)), ('knn', KNeighborsClassifier())]
clf = VotingClassifier(models)
clf.fit(X_train, y_train)
print('train_acc:', clf.score(X_train, y_train))
print('test_acc:', clf.score(X_test, y_test))
print('test_label_counts:', y_test.value_counts().to_dict())
cases = [
    {'name': 'freebitcoin_now','screen_name': 'getmoney_fast','description': 'Win Bitcoin now! Click link and get rich fast','created_at': 'Wed Mar 10 12:00:00 +0000 2021','location': 'Unknown','default_profile': '1','statuses_count': '5','followers_count': '2','friends_count': '10'},
    {'name': 'Jessica Martin','screen_name': 'jessica_martin','description': 'Product manager, traveler, coffee lover. Sharing thoughts on tech and life.','created_at': 'Mon Apr 15 14:20:10 +0000 2014','location': 'New York, USA','default_profile': '0','statuses_count': '542','followers_count': '1832','friends_count': '410'},
]
for case in cases:
    text = build_feature_text(case)
    pred = clf.predict(vectorizer.transform([text]))[0]
    print('case', case['name'], 'pred', pred)
