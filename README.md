Fake Profile Detection on Social Networks using ML & NLP
Overview

This project is a Django-based web application designed to detect fake profiles on social networking platforms using Machine Learning (ML) and Natural Language Processing (NLP).

The system analyzes social media profile attributes such as profile ID, username, follower count, friend count, account creation details, and other metadata to classify profiles as:

Fake Profile
Genuine Profile

This project was developed as a research-oriented application inspired by an IEEE Conference paper (May 2022), combining web development, machine learning, and NLP techniques.

Features
User Module (Remote_User)
User Registration & Login

Users can:

Create new accounts
Login securely
Manage their profile details
Fake Profile Prediction

Users can enter social media profile details such as:

Profile ID
Profile Name
Screen Name
Followers Count
Friends Count
Statuses Count
Account Creation Date
Other profile-related attributes

The system then predicts whether the profile is:

Fake
Genuine
ML-Based Prediction

The prediction system:

Uses NLP preprocessing techniques
Cleans text data by removing:
URLs
Punctuation
Special characters
Applies ML classification models
Returns prediction results instantly
Admin Module (Service_Provider)
Admin Authentication

Default credentials:

Username: Admin
Password: Admin
Model Training

Admin can:

Train machine learning models
Compare classifier performances
Store accuracy results in the database
Implemented Algorithms
Support Vector Machine (SVM)
K-Nearest Neighbors (KNN)
Naive Bayes
Voting Classifier (SVM + KNN)
Analytics Dashboard

Admin dashboard includes:

Fake vs Genuine profile ratios
Prediction statistics
Accuracy comparison charts
User prediction history
Dataset Management

Admin can:

View registered users
View prediction records
Download datasets/results in Excel format
Machine Learning Workflow
Dataset

The project uses a Twitter profile dataset:

Profile_Datasets.csv

Dataset labels:

0 → Fake Profile
1 → Genuine Profile
Preprocessing

The dataset undergoes:

Text cleaning
Tokenization
Feature extraction using CountVectorizer
Training Process
Dataset split:
67% Training
33% Testing
Model training using scikit-learn
Prediction Technique

The application primarily uses:

Profile ID
Social profile metadata
NLP-processed text features

for classification.

Technologies Used
Backend
Python
Django 3.0
Frontend
HTML
CSS
Bootstrap
JavaScript
Database
MySQL
Machine Learning & NLP
scikit-learn
pandas
numpy




Project Structure
Fake-Profile-Detection/
│
├── Remote_User/
│   ├── User authentication
│   ├── Prediction module
│   └── User dashboards
│
├── Service_Provider/
│   ├── Admin login
│   ├── ML model training
│   ├── Analytics
│   └── Dataset management
│
├── templates/
├── static/
├── media/
├── Profile_Datasets.csv
├── manage.py
└── requirements.txt
Database Models
ClientRegister_Model

Stores user registration details.

profile_identification_type

Stores:

Profile inputs
Prediction outputs
detection_accuracy

Stores ML model accuracy percentages.

detection_ratio

Stores:

Fake profile percentages
Genuine profile percentages
Installation Guide
1. Clone the Repository
git clone https://github.com/your-username/fake-profile-detection.git
cd fake-profile-detection
2. Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Database

Update database settings in:

settings.py

Example:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fake_profile_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
5. Run Migrations
python manage.py makemigrations
python manage.py migrate
6. Start the Server
python manage.py runserver

Open:

http://127.0.0.1:8000/

Future Enhancements
Deep Learning integration
Real-time Twitter API integration
Advanced NLP feature extraction
Multi-platform fake account detection
Improved accuracy using ensemble methods
