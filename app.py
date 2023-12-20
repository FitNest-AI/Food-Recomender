from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime
import json
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

secret_key = os.getenv("SECRET_KEY")

def is_login():
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    return decoded_token['id']

def calculate_age(profile):
    datenow = datetime.now()
    age = datenow.year - profile['dateOfBirth'].year
    if profile['dateOfBirth'].month > datenow.month or (profile['dateOfBirth'].month == datenow.month and profile['dateOfBirth'].day > datenow.day):
        return age - 1
    return age

def calculate_bmr(profile, age):
    # (10 x berat badan dalam kg) + (6.25 x tinggi badan dalam cm) – (5 x usia dalam tahun) + 5
    if(profile['gender'] == 'man'):
        return (10 * profile['weight']) + (6.25 * profile['height']) - (5 * age) + 5

    # (10 x berat badan dalam kg) + (6.25 x tinggi badan dalam cm) – (5 x usia dalam tahun) – 161.
    if(profile['gender'] == 'man'):
        return (10 * profile['weight']) + (6.25 * profile['height']) - (5 * age) - 161
    
def calculate_carbs(goal, bmr):
    print(goal)

    return goal

def calculate_calories(profile, bmr):
    level = mongo.db.levels.find_one({'_id': ObjectId(profile['levelId'])})

    if(level['name'] == 'easy'):
        return bmr * 1.2

    if(level['name'] == 'medium'):
        return bmr * 1.55

    if(level['name'] == 'hard'):
        return bmr * 1.725   
    
def persentase_carbs_fat_protein(profile):
    goal = mongo.db.goals.find({'_id': {'$in': profile['goalId']}})[0]

    if(goal['name'] == 'gain muscle'):
        return {
            'protein': 0.2,
            'fat': 0.5,
            'carbs': 0.3,
        }
    
    if(goal['name'] == 'lose weight'):
        return {
            'protein': 0.5,
            'fat': 0.2,
            'carbs': 0.3,
        }
    
    if(goal['name'] == 'keep fit' or goal['name'] == 'improving posture'):
        return {
            'protein': 3.3,
            'fat': 3.3,
            'carbs': 3.3,
        }

def calculate_nutrition(calories, persentase):

    portion = 3

    return{
        'carbs': persentase['carbs'] * (calories / 4) / portion,
        'fat': persentase['fat'] * (calories / 9) / portion,
        'protein': persentase['protein'] * (calories / 4) / portion,
    }

def get_recomendation(user_data: list, search_query='', page=1, per_page=10):
    """Get the recomendation for the user based on the user data
    Args:
        user_data (list): The user data [calories,carbs,fat,protein,type]
        amount (int): The amount of recomendations
    Returns:
        json: The recomendation in json format
        """     
    # Load the dataset
    main = pd.read_csv('https://storage.googleapis.com/developmentfitnest-bucket/Dataset/food.csv')
    df = main.copy()

    #filter
    if user_data[4] != 0:
        df = df[df['type'] == user_data[4]].reset_index(drop=True)
        main = main[main['type'] == user_data[4]].reset_index(drop=True)
        
    user_data = user_data[:4]
    df = df.drop(['label','type'], axis=1)
    #clear
    main["label"] = main["label"].str.replace(" (","(").str.split("(").str[0]
    #add image url
    url = []
    for food in main['label']:
        url.append("https://https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/" 
                   + food.lower().replace(" ", "%20") + ".jpg")
    main["image"] = url
    
    X = df.values
    model = NearestNeighbors(n_neighbors=len(df), algorithm='ball_tree')
    model.fit(X)
    
    #data
    user_data = np.array(user_data).reshape(1, -1)
    _, indices = model.kneighbors(user_data)

    recommended_foods = main.iloc[indices[0]]

    # Filter on search query
    if search_query:
        main = main[main['label'].str.contains(search_query, case=False)]

    # Implement pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    recommended_foods = main.iloc[start_index:end_index]

    data = json.dumps(recommended_foods.to_dict(orient='records'), indent=4)

    return data

@app.route('/', methods=['GET'])
def get_food():
    userId = is_login()
    profile = mongo.db.profiles.find_one({'userId': ObjectId(userId)})
    dietPref = mongo.db.diet_prefs.find_one({'_id': profile['dietPrefId']})

    age = calculate_age(profile)
    bmr = calculate_bmr(profile, age)

    print(dietPref['name'])

    per_carbs_fat_protein = persentase_carbs_fat_protein(profile)
    calories = calculate_calories(profile, bmr)
    types = 1 if dietPref['name'] != "non vegan" else 0

    cal_nutrition = calculate_nutrition(calories, per_carbs_fat_protein)

    # search query from the request
    search_query = request.args.get('q', default='', type=str)

    # page number
    page = request.args.get('page', default=1, type=int)
    per_page = 6  # Number of items per page

    # Get recommendation
    recommendation = get_recomendation(
        [float(nutrition) for nutrition in [calories / 3, cal_nutrition['carbs'], cal_nutrition['fat'],
                                            cal_nutrition['protein'], types]],
        search_query=search_query,
        page=page,
        per_page=per_page
    )

    # Convert the recommendation data to JSON
    recommendation_json = json.loads(recommendation)

    # Implement pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_recommendation = recommendation_json[start_index:end_index]

    # Total pages
    total_pages = int(len(recommendation_json) / per_page) + 1

    response = {
        'total_pages': total_pages,
        'current_page': page,
        'recommendation': paginated_recommendation
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5200)