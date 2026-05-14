# Fake Profile Detection on Social Networks using ML & NLP

## Overview
This project is a Django-based web application designed to detect fake profiles on social networking platforms using Machine Learning (ML) and Natural Language Processing (NLP).

The system analyzes social media profile attributes such as profile ID, username, follower count, friend count, account creation details, and other metadata to classify profiles as:

- **Fake Profile**
- **Genuine Profile**

This project was developed as a research-oriented application inspired by an IEEE Conference paper (May 2022), combining web development, machine learning, and NLP techniques.

---

# Features

## User Module (Remote_User)

### User Registration & Login
Users can:
- Create new accounts
- Login securely
- Manage their profile details

### Fake Profile Prediction
Users can enter social media profile details such as:
- Profile ID
- Profile Name
- Screen Name
- Followers Count
- Friends Count
- Statuses Count
- Account Creation Date
- Other profile-related attributes

The system then predicts whether the profile is:
- Fake
- Genuine

### ML-Based Prediction
The prediction system:
- Uses NLP preprocessing techniques
- Cleans text data by removing:
  - URLs
  - Punctuation
  - Special characters
- Applies ML classification models
- Returns prediction results instantly

---

# Admin Module (Service_Provider)

## Admin Authentication
Default credentials:

Username: Admin  
Password: Admin

## Model Training
Admin can:
- Train machine learning models
- Compare classifier performances
- Store accuracy results in the database

### Implemented Algorithms
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes
- Voting Classifier (SVM + KNN)

---

## Analytics Dashboard
Admin dashboard includes:
- Fake vs Genuine profile ratios
- Prediction statistics
- Accuracy comparison charts
- User prediction history

---

## Dataset Management
Admin can:
- View registered users
- View prediction records
- Download datasets/results in Excel format

---

# Machine Learning Workflow

## Dataset
The project uses a Twitter profile dataset:

`Profile_Datasets.csv`

Dataset labels:
- `0` → Fake Profile
- `1` → Genuine Profile

---

## Preprocessing
The dataset undergoes:
- Text cleaning
- Tokenization
- Feature extraction using CountVectorizer

---

## Training Process
- Dataset split:
  - 67% Training
  - 33% Testing
- Model training using scikit-learn

---

## Prediction Technique
The application primarily uses:
- Profile ID
- Social profile metadata
- NLP-processed text features

for classification.

---

# Technologies Used

## Backend
- Python
- Django 3.0

## Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

## Database
- MySQL

## Machine Learning & NLP
- scikit-learn
- pandas
- numpy

---

# Project Structure

```text
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
