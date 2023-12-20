## Fetch Food Recommendation

**HTTP Request**

```
    GET /?q={{workout_name}}&page={{page}}
```

**Query**

| Parameter | Description                         |
| :-------- | :---------------------------------- |
| `q`       | The workout name for deletion.       |
| `page`    | The page number for pagination.      |

**Response Body**

| Parameter          | Description                                                               |
| :------------------ | :------------------------------------------------------------------------ |
| `recommendation`   | An array of recommended food items.                                      |
| `current_page`     | The current page number in the paginated response.                        |
| `total_pages`      | The total number of pages available for the given query.                  |


**Example**

```
curl GET "{{base_url}}/?q={{workout_name}}&page={{page}}"
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