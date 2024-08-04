##pip install numpy scikit-learn
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import math
from .models import db, User

def get_coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'YourAppName/1.0 (esdf@gmail.com)'  # Replace with your app name and email
    }
    response = requests.get(url, params=params, headers=headers)
    
    #response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"Error: {response.status_code}")
    
    if data:
        location = data[0]
        return location['lat'], location['lon']
    else:
        raise Exception("Error fetching coordinates or address not found")


def update_user_location(user_id, address):
    lat, lng = get_coordinates(address)
    user = User.query.get(user_id)
    user.location_lat = lat
    user.location_lng = lng
    db.session.commit()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_distance(user1_id, user2_id):
    user1 = User.query.get(user1_id)
    user2 = User.query.get(user2_id)
    return haversine(user1.location_lat, user1.location_lng, user2.location_lat, user2.location_lng)



def get_user_data():
    users = User.query.all()
    user_data = [
        {
            'id': user.id,
            'age': user.age,
            'location': user.location,
            'description': user.selfDescription,
            'field': user.field,
            'goals': user.goals
        }
        for user in users
    ]
    return user_data

def age_similarity(age1, age2):
    return 1 - abs(age1 - age2) / 100

def location_similarity(loc1, loc2):
    return 1 if loc1 == loc2 else 0

def description_similarity(desc1, desc2):
    tfidf = TfidfVectorizer().fit_transform([desc1, desc2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]