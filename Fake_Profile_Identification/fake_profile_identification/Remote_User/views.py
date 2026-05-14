from django.shortcuts import render, redirect
import re
import string
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

from Remote_User.models import ClientRegister_Model, profile_identification_type


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


def train_profile_model():
    """Train improved model with TF-IDF text features and numeric features."""
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
    
    models = [
        ('lr1', LogisticRegression(max_iter=1000, C=0.1, class_weight='balanced')),
        ('lr2', LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')),
    ]
    classifier = VotingClassifier(models, voting='soft')
    classifier.fit(X_train, y_train)
    
    return vectorizer, scaler, classifier


def login(request):
    if request.method == 'POST' and 'submit1' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username, password=password)
            request.session['userid'] = enter.id
            return redirect('ViewYourProfile')
        except ClientRegister_Model.DoesNotExist:
            pass
    return render(request, 'RUser/login.html')


def Register1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        if not ClientRegister_Model.objects.filter(username=username).exists():
            ClientRegister_Model.objects.create(
                username=username,
                email=email,
                password=password,
                phoneno=phoneno,
                country=country,
                state=state,
                city=city,
            )
            return redirect('login')

    return render(request, 'RUser/Register1.html')


def ViewYourProfile(request):
    userid = request.session.get('userid')
    if userid is None:
        return redirect('login')

    obj = ClientRegister_Model.objects.get(id=userid)
    return render(request, 'RUser/ViewYourProfile.html', {'object': obj})


def Predict_Profile_Identification_Status(request):
    prediction = None
    if request.method == 'POST':
        form_data = {
            'prof_idno': request.POST.get('prof_idno', '').strip(),
            'name': request.POST.get('name', '').strip(),
            'screen_name': request.POST.get('screen_name', '').strip(),
            'statuses_count': request.POST.get('statuses_count', '').strip(),
            'followers_count': request.POST.get('followers_count', '').strip(),
            'friends_count': request.POST.get('friends_count', '').strip(),
            'created_at': request.POST.get('created_at', '').strip(),
            'location': request.POST.get('location', '').strip(),
            'default_profile': request.POST.get('default_profile', '').strip(),
            'prf_image_url': request.POST.get('prf_image_url', '').strip(),
            'prf_banner_url': request.POST.get('prf_banner_url', '').strip(),
            'prf_bgimg_https': request.POST.get('prf_bgimg_https', '').strip(),
            'prf_text_color': request.POST.get('prf_text_color', '').strip(),
            'profile_image_url_https': request.POST.get('profile_image_url_https', '').strip(),
            'prf_bg_title': request.POST.get('prf_bg_title', '').strip(),
            'profile_background_image_url': request.POST.get('profile_background_image_url', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'Prf_updated': request.POST.get('Prf_updated', '').strip(),
        }

        vectorizer, scaler, classifier = train_profile_model()
        input_text = build_feature_text(form_data)
        input_numeric = extract_numeric_features(form_data)
        
        X_text = vectorizer.transform([input_text])
        X_numeric = scaler.transform([input_numeric])
        
        X_input = hstack([X_text, X_numeric])
        
        prediction_label = classifier.predict(X_input)[0]
        prediction = 'Genuine Profile' if prediction_label == 1 else 'Fake Profile'

        profile_identification_type.objects.create(
            prof_idno=form_data['prof_idno'],
            name=form_data['name'],
            screen_name=form_data['screen_name'],
            statuses_count=form_data['statuses_count'],
            followers_count=form_data['followers_count'],
            friends_count=form_data['friends_count'],
            created_at=form_data['created_at'],
            location=form_data['location'],
            default_profile=form_data['default_profile'],
            prf_image_url=form_data['prf_image_url'],
            prf_banner_url=form_data['prf_banner_url'],
            prf_bgimg_https=form_data['prf_bgimg_https'],
            prf_text_color=form_data['prf_text_color'],
            profile_image_url_https=form_data['profile_image_url_https'],
            prf_bg_title=form_data['prf_bg_title'],
            profile_background_image_url=form_data['profile_background_image_url'],
            description=form_data['description'],
            Prf_updated=form_data['Prf_updated'],
            Prediction=prediction,
        )

    return render(request, 'RUser/Predict_Profile_Identification_Status.html', {'objs': prediction})

