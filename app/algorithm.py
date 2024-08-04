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
from datetime import datetime, timedelta

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
        return None


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

def add_like(user_id, liked_user_id, is_like=True):
    if user_id == liked_user_id:
        raise Exception("You cannot like/dislike yourself.")
    
    existing_like = Like.query.filter_by(user_id=user_id, liked_user_id=liked_user_id).first()
    if existing_like:
        existing_like.is_like = is_like
        db.session.commit()
        return "Like/Dislike updated"
    
    new_like = Like(user_id=user_id, liked_user_id=liked_user_id, is_like=is_like)
    db.session.add(new_like)
    db.session.commit()
    return "Like/Dislike added"

def remove_like(user_id, liked_user_id):
    like_to_remove = Like.query.filter_by(user_id=user_id, liked_user_id=liked_user_id).first()
    if like_to_remove:
        db.session.delete(like_to_remove)
        db.session.commit()
        return "Like/Dislike removed"
    return "Like/Dislike does not exist"

def calculate_similarity(user1, user2, user_id):
    age_sim = age_similarity(user1.age, user2.age)
    loc_sim = location_similarity(user1, user2)
    desc_sim = description_similarity(user1.self_description, user2.self_description)
    field_sim = field_similarity(user1.field, user2.field)
    goals_sim = goals_similarity(user1.goals, user2.goals)
    
    base_similarity = (0.2 * age_sim) + (0.1 * loc_sim) + (0.7 * desc_sim) + (0.5 * field_sim) + (0.7 * goals_sim)

    recent_likes = Like.query.filter_by(user_id=user_id, liked_user_id=user2.id).order_by(Like.timestamp.desc()).first()
    if recent_likes and recent_likes.is_like:
        base_similarity += 0.5
    elif recent_likes and not recent_likes.is_like:
        base_similarity -= 0.5
    
    
    if Like.query.filter_by(user_id=user2.id, liked_user_id=user1.id, is_like=True).first():
        base_similarity += 0.3 #start chat maybe?

    return base_similarity

def recommend_user(target_user_id):
    target_user = User.query.get(target_user_id)
    all_users = User.query.filter(User.id != target_user_id).all()
    
    best_recommendation = None
    best_similarity = -float('inf')
    
    for user in all_users:
        similarity = calculate_similarity(target_user, user, target_user_id)
        if similarity > best_similarity:
            best_similarity = similarity
            best_recommendation = user

    return best_recommendation
