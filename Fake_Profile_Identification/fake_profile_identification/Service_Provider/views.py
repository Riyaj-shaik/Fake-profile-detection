from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
import string
import pandas as pd
import numpy as np
import xlwt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from scipy.sparse import hstack

from Remote_User.models import ClientRegister_Model, profile_identification_type, detection_ratio, detection_accuracy


def clean_text(text):
    if pd.isna(text):
        return ""
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
    text = re.sub(r'Ã¢â‚¬â€', '', text)
    return ' '.join(text.split())


def build_feature_text(item):
    parts = [
        clean_text(item.get('name')),
        clean_text(item.get('screen_name')),
        clean_text(item.get('description')),
        clean_text(item.get('location')),
    ]
    return ' '.join(part for part in parts if part)


def extract_numeric_features(item):
    """Extract numeric features and compute ratios."""
    try:
        statuses = float(item.get('statuses_count', 0) or 0)
        followers = float(item.get('followers_count', 0) or 0)
        friends = float(item.get('friends_count', 0) or 0)
        default_profile = float(item.get('default_profile', 1) or 1)
        
        follower_friend_ratio = followers / (friends + 1)
        status_level = statuses / (followers + 1)
        friend_to_follower = friends / (followers + 1)
        
        return np.array([
            statuses,
            followers,
            friends,
            default_profile,
            follower_friend_ratio,
            status_level,
            friend_to_follower,
        ])
    except:
        return np.array([0, 0, 0, 1, 0, 0, 0])


def serviceproviderlogin(request):
    if request.method == 'POST':
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == 'Admin' and password == 'Admin':
            return redirect('View_Remote_Users')
    return render(request, 'SProvider/serviceproviderlogin.html')


def View_Profile_Identity_Prediction(request):
    obj = profile_identification_type.objects.all()
    return render(request, 'SProvider/View_Profile_Identity_Prediction.html', {'objs': obj})


def View_Profile_Identity_Prediction_Ratio(request):
    detection_ratio.objects.all().delete()
    total_count = profile_identification_type.objects.count()
    if total_count > 0:
        for label in ['Genuine Profile', 'Fake Profile']:
            count = profile_identification_type.objects.filter(Prediction=label).count()
            ratio = (count / total_count) * 100
            if ratio > 0:
                detection_ratio.objects.create(names=label, ratio=ratio)
    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Profile_Identity_Prediction_Ratio.html', {'objs': obj})


def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})


def charts(request, chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, 'SProvider/charts.html', {'form': chart1, 'chart_type': chart_type})


def charts1(request, chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, 'SProvider/charts1.html', {'form': chart1, 'chart_type': chart_type})


def likeschart(request, like_chart):
    charts = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, 'SProvider/likeschart.html', {'form': charts, 'like_chart': like_chart})


def likeschart1(request, like_chart):
    charts = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, 'SProvider/likeschart1.html', {'form': charts, 'like_chart': like_chart})


def Download_Trained_DataSets(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Predicted_Datasets.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for my_row in profile_identification_type.objects.all():
        row_num += 1
        ws.write(row_num, 0, my_row.prof_idno, font_style)
        ws.write(row_num, 1, my_row.name, font_style)
        ws.write(row_num, 2, my_row.screen_name, font_style)
        ws.write(row_num, 3, my_row.statuses_count, font_style)
        ws.write(row_num, 4, my_row.followers_count, font_style)
        ws.write(row_num, 5, my_row.friends_count, font_style)
        ws.write(row_num, 6, my_row.created_at, font_style)
        ws.write(row_num, 7, my_row.location, font_style)
        ws.write(row_num, 8, my_row.default_profile, font_style)
        ws.write(row_num, 9, my_row.prf_image_url, font_style)
        ws.write(row_num, 10, my_row.prf_banner_url, font_style)
        ws.write(row_num, 11, my_row.prf_bgimg_https, font_style)
        ws.write(row_num, 12, my_row.prf_text_color, font_style)
        ws.write(row_num, 13, my_row.profile_image_url_https, font_style)
        ws.write(row_num, 14, my_row.prf_bg_title, font_style)
        ws.write(row_num, 15, my_row.profile_background_image_url, font_style)
        ws.write(row_num, 16, my_row.description, font_style)
        ws.write(row_num, 17, my_row.Prf_updated, font_style)
        ws.write(row_num, 18, my_row.Prediction, font_style)
    wb.save(response)
    return response


def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()
    df = pd.read_csv('Profile_Datasets.csv')
    df = df.fillna('')
    df['text_features'] = df.apply(build_feature_text, axis=1)
    df['numeric_features'] = df.apply(lambda row: extract_numeric_features(row), axis=1)
    
    y = df['Label'].astype(int)
    
    text_data = df['text_features'].values
    numeric_data = np.array(df['numeric_features'].tolist())
    
    vectorizer = TfidfVectorizer(lowercase=True, max_features=500, min_df=2, max_df=0.8)
    X_text = vectorizer.fit_transform(text_data)
    
    scaler = StandardScaler()
    X_numeric = scaler.fit_transform(numeric_data)
    
    X = hstack([X_text, X_numeric])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    lr_clf1 = LogisticRegression(max_iter=1000, C=0.1, class_weight='balanced')
    lr_clf1.fit(X_train, y_train)
    predict_lr1 = lr_clf1.predict(X_test)
    lr1_acc = accuracy_score(y_test, predict_lr1) * 100
    detection_accuracy.objects.create(names='Logistic Regression (C=0.1)', ratio=lr1_acc)

    lr_clf2 = LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')
    lr_clf2.fit(X_train, y_train)
    predict_lr2 = lr_clf2.predict(X_test)
    lr2_acc = accuracy_score(y_test, predict_lr2) * 100
    detection_accuracy.objects.create(names='Logistic Regression (C=1.0)', ratio=lr2_acc)

    models = [
        ('lr1', LogisticRegression(max_iter=1000, C=0.1, class_weight='balanced')),
        ('lr2', LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')),
    ]
    voting_clf = VotingClassifier(models, voting='soft')
    voting_clf.fit(X_train, y_train)
    predict_voting = voting_clf.predict(X_test)
    voting_acc = accuracy_score(y_test, predict_voting) * 100
    detection_accuracy.objects.create(names='Voting Classifier (Soft)', ratio=voting_acc)

    obj = detection_accuracy.objects.all()
    return render(request, 'SProvider/Train_Test_DataSets.html', {'objs': obj})














