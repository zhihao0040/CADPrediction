import requests

url = 'http://localhost:5000/predict'
body = {
    'ca': 2,
    'cp': 3,
    'exang': 0, 
    'oldpeak': 5, 
    'sex': 1, 
    'slope': 3, 
    'thal': 7, 
    'thaldur': 11, 
    'thalach': 200, 
    'restecg': 2, 
    'age': 75, 
    'chol': 400, 
    'md': 1
}

response = requests.post(url, data=body)
print(response.json())