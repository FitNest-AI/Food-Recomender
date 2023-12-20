from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import jwt
import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

LEVEL_MULTIPLIER = {'easy': 1, 'medium': 2, 'hard': 3}

def load_environment_variables():
    load_dotenv()

def get_recommendation(database, workout_data, level="easy", target=["abs"]):
    # Data preparation
    prepared_data = prepare_data_for_recommendation(workout_data, level)
    
    # Nearest Neighbors algorithm
    recommendations = find_nearest_neighbors(database, prepared_data, target)
    
    return [database[index] for index in recommendations]

def prepare_data_for_recommendation(workout_list, level):
    # Data manipulation
    temporary = prepare_temporary_data(workout_list, level)
    df = pd.DataFrame(temporary)
    
    # Level filtering
    main = filter_data_by_level(df, level)
    
    target_muscle = main.columns.tolist()
    user_data = generate_user_data(df, target_muscle)
    
    return main.values, user_data

def prepare_temporary_data(workout_list, level):
    temporary = []
    for index, data in enumerate(workout_list):
        temp_dict = data[0]
        temp_dict['level'] = data[1]
        temp_dict['index'] = index
        temporary.append(temp_dict)

    df = pd.DataFrame(temporary)
    return df.copy()

def filter_data_by_level(dataframe, level):
    if level == "easy":
        return dataframe[dataframe['level'] == "easy"]
    elif level == "medium":
        return dataframe[dataframe['level'] != "hard"]
    else:
        return dataframe

def generate_user_data(dataframe, target_muscle):
    user_data = []
    for muscle in target_muscle:
        target_muscle_mean = 0
        if muscle in target:
            target_muscle_mean = dataframe[muscle].max()
        user_data.append(target_muscle_mean)

    return user_data

def find_nearest_neighbors(database, prepared_data, target):
    X, user_data = prepared_data
    
    # Apply Min-Max scaling to normalize the data
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    user_data_scaled = scaler.transform([user_data])
    
    model = NearestNeighbors(n_neighbors=len(X_scaled), algorithm='ball_tree')
    model.fit(X_scaled)
    _, indices = model.kneighbors(user_data_scaled)
    
    return indices[0]

@app.route('/', methods=['GET'])
def get_workout():
    secret_key = os.getenv("SECRET_KEY")
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

    profile = mongo.db.profiles.find_one({'userId': ObjectId(decoded_token['id'])})
    level = mongo.db.levels.find_one({'_id': ObjectId(profile['levelId'])})
    
    target_muscle_ids = [ObjectId(id) for id in profile['targetMuscleId']]
    target_muscles = mongo.db.target_muscles.find({'_id': {'$in': target_muscle_ids}})
    
    target_muscle_names = [muscle['name'] for muscle in target_muscles]

    workouts = mongo.db.workouts.find()
    result = prepare_result_data(workouts, level, target_muscle_names)

    print(type(result)) # type list

    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=6, type=int)

    # Search parameter
    search_query = request.args.get('q', default='', type=str)

    # Apply search to the result
    if search_query:
        result = [workout for workout in result if search_query.lower() in workout['name'].lower()]

    # Calculate the starting index for slicing
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Apply pagination to the result
    paginated_result = result[start_index:end_index]

    response = {
        'success': True,
        'message': 'Workout data fetch successful',
        'data': {
            'workout': paginated_result,
            'count': len(result),
            'page': page,
            'per_page': per_page,
            'search_query': search_query,
        }
    }

    return jsonify(response)

    return jsonify(response)

    return jsonify(response)



def prepare_result_data(workouts, level, target_muscle_names):
    result = []
    for workout in workouts:
        result.append(prepare_workout_data(workout, level, target_muscle_names))
    return result

def prepare_workout_data(workout, level, target_muscle_names):
    return {
        '_id': str(workout['_id']),
        'name': workout['name'],
        'desc': workout['desc'],
        'rest': workout['rest'],
        'day': workout['day'],
        'time': workout['time'],
        'level': get_most_common_level(workout['moveset']),
        'point': calculate_points_by_target_muscle(workout['moveset']),
        'moveset': prepare_moveset_data(workout['moveset']),
        'userId': str(workout['userId']),
    }

def prepare_moveset_data(moveset):
    return [
        {
            'rep': move['rep'],
            'set': move['set'],
            'exerciseId': get_exercise_data(move['exerciseId'])
        } for move in moveset
    ]

def get_exercise_data(exercise_id):
    exercise = mongo.db.exercises.find_one({'_id': ObjectId(exercise_id)})
    if exercise:
        return {
            '_id': str(exercise['_id']),
            'name': exercise['name'],
            'desc': exercise['desc'],
            'image': exercise['image'],
            'levelId': get_level_data(exercise['levelId']),
            'targetMuscleId': get_target_muscle_data(exercise['targetMuscleId']),
            'direction': exercise['direction'],
            'orientation': exercise['orientation'],
            'instruction': exercise['instruction'],
            'start': exercise['start'],
            'end': exercise['end'],
        }
    else:
        return None

def get_level_data(level_id):
    level = mongo.db.levels.find_one({'_id': ObjectId(level_id)})
    if level:
        return {
            '_id': str(level['_id']),
            'name': level['name'],
        }
    else:
        return None

def get_target_muscle_data(target_muscle_ids):
    result = []
    for target_muscle_id in target_muscle_ids:
        target_muscle = mongo.db.target_muscles.find_one({'_id': ObjectId(target_muscle_id)})
        if target_muscle:
            result.append({
                '_id': str(target_muscle['_id']),
                'name': target_muscle['name'],
            })

    return result if result else None

def get_most_common_level(moveset):
    levels = [get_exercise_data(move['exerciseId'])['levelId']['name'] for move in moveset]
    result = {}
    
    for level in levels:
        result[level] = result.get(level, 0) + 1
    
    most_common_level = max(result, key=result.get, default=None)
    
    return most_common_level

def calculate_points_by_target_muscle(moveset):
    points_by_target_muscle = {}

    for move in moveset:
        exercise_data = get_exercise_data(move['exerciseId'])
        target_muscles = exercise_data.get('targetMuscleId', [])
        level_data = exercise_data.get('levelId', {})
        level_name = level_data.get('name', 'easy')
        level_number = LEVEL_MULTIPLIER.get(level_name, 1)

        # Fetch all target muscles from the database
        target_muscle_non = mongo.db.target_muscles.find()

        # Initialize points for all target muscles with 0
        for target_muscle in target_muscle_non:
            target_muscle_name = target_muscle['name']
            points_by_target_muscle.setdefault(target_muscle_name, 0)

        for target_muscle in target_muscles:
            target_muscle_name = target_muscle['name']
            rep = move['rep']
            set_count = move['set']
            points = (rep * set_count) * level_number

            # Update points for the specific target muscle
            points_by_target_muscle[target_muscle_name] += points


    return points_by_target_muscle

if __name__ == '__main__':
    app.run(debug=True)