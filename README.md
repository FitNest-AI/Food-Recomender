## How to run this API on your local machine 💻
If you want to run this API Server on your local machine, you need to do these steps:
- First, clone this repository. `git clone https://github.com/FitNest-AI/Food-Recomender.git`
- Second, open the terminal and go to this project's root directory.
- Third, type `pip install requirement.txt` in your terminal and hit enter button.
- Fourth, type `flask run` in your terminal and hit enter button.
- Finally, the server will run on your http://localhost:3000

## How to deploy this API to Cloud Run 🚀
If you want to deploy this API server to Cloud Run, you need to follow this steps:
- First, open your Google Cloud Console. https://console.cloud.google.com/
- Second, open the Cloud Shell at the right top corner in the Google Cloud Console. Make sure you enable Cloud Run API and Cloud Build API before.
- Third, copy the command below to cloning this repository into the Cloud Shell.
 ```
git clone https://github.com/FitNest-AI/Food-Recomender.git
 ```
- Fourth, add the .env file with Variables to the Food Recomender folder
```
MONGO_URI: <your MONGO_URI>
SECRET_KEY: <your SECRET_KEY>
```

- Fifth, go to this project's root directory in the Cloud Shell.
```
cd fitnest-backend
export PROJECT_ID= <Your GCP project ID>
```
- Sixth, copy the command below to build the image container and upload it to the Container Registry.
 ```
gcloud builds submit \
  --tag asia.gcr.io/$PROJECT_ID/Food-Recomender
  ```
- seventh, copy the command below to deploy your image container to Cloud Run.
 ```
 gcloud run deploy fitnest-backend \
  --image asia.gcr.io/$PROJECT_ID/Food-Recomender \
  --platform managed \
  --cpu=1 \
  --memory=512Mi \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --max-instances=3 \
  --port=5200
 ```
- Finally, your API server will be deploy to Cloud Run and you will get the URL in the Cloud Shell to access the your server.


## Fetch Food Recommendation

**HTTP Request**

```
    GET /?q={{food_name}}&page={{page}}
```

**Query**

| Parameter | Description                         |
| :-------- | :---------------------------------- |
| `q`       | The food name for search.       |
| `page`    | The page number for pagination.      |

**Response Body**

| Parameter          | Description                                                               |
| :------------------ | :------------------------------------------------------------------------ |
| `recommendation`   | An array of recommended food items.                                      |
| `current_page`     | The current page number in the paginated response.                        |
| `total_pages`      | The total number of pages available for the given query.                  |


**Example**

```
curl GET "{{base_url}}/?q={{food_name}}&page={{page}}"
```

```JSON
   {
  "recommendation": [
    {
      "Calories": 52.0,
      "Carbs": 2.11,
      "Fat": 4.47,
      "Protein": 1.6,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/biji%20wijen.jpg",
      "label": "Biji Wijen",
      "type": 1
    },
    {
      "Calories": 578.0,
      "Carbs": 19.74,
      "Fat": 50.64,
      "Protein": 21.26,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/kacang%20almond.jpg",
      "label": "Kacang Almond",
      "type": 1
    },
    {
      "Calories": 876.0,
      "Carbs": 30.64,
      "Fat": 79.95,
      "Protein": 23.44,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/kacang%20campuran.jpg",
      "label": "Kacang Campuran",
      "type": 1
    },
    {
      "Calories": 471.0,
      "Carbs": 33.55,
      "Fat": 25.4,
      "Protein": 35.22,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/kacang%20kedelai.jpg",
      "label": "Kacang Kedelai",
      "type": 1
    },
    {
      "Calories": 581.0,
      "Carbs": 30.16,
      "Fat": 47.77,
      "Protein": 16.84,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/kacang%20mete.jpg",
      "label": "Kacang Mete",
      "type": 1
    },
    {
      "Calories": 567.0,
      "Carbs": 16.13,
      "Fat": 49.24,
      "Protein": 25.8,
      "image": "https://github.com/FitNest-AI/Machine-Learning/blob/main/Datasets/Tracker/images/kacang%20tanah.jpg",
      "label": "Kacang Tanah",
      "type": 1
    }
  ],
  "current_page": 1,
  "total_pages": 2
}

```
