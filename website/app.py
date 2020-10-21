from flask import Flask, render_template, request, url_for, redirect, session
from flask_restful import Api, Resource, reqparse
import pandas as pd
import pickle

def convert_float(arr):
    temp = []
    for item in arr:
        temp.append(float(item))
    return temp
app = Flask(__name__)
app.static_folder = 'static'
API = Api(app)

knn_model = pickle.load(open('models/SVM.pkl','rb'))
lda_model = pickle.load(open('models/LDA.pkl','rb'))
svm2_model = pickle.load(open('models/SVM2.pkl','rb'))
svm_model = pickle.load(open('models/SVM.pkl','rb'))
voting_model = pickle.load(open('models/Voting.pkl','rb'))
voting2_model = pickle.load(open('models/Voting2.pkl','rb'))
models = [svm_model,lda_model,knn_model,svm2_model,voting_model,voting2_model]
models_name = ["SVM", "LDA", "KNN", "SVM 2", "Voting", "Voting 2"]

chosen_feature = open('models/chosen_feature.txt','r')
feature = chosen_feature.readline()
min_data = chosen_feature.readline()
range_data = chosen_feature.readline()
chosen_feature.close()

feature = feature.strip('\n').split(' ')
min_data = min_data.strip('\n').split(' ')
range_data = range_data.strip('\n').split(' ')
min_data = convert_float(min_data)
range_data = convert_float(range_data)

def model_predict(data_dict):
    model_id = int(data_dict["md"])
    model = models[model_id]
    predict_data = {}
    for i in range (len(feature)):
        predict_data[feature[i]] = [(float(data_dict[feature[i]])-min_data[i])/range_data[i]]        
    df = pd.DataFrame(predict_data)
    if model_id == 3 or model_id==5:
        svm_result = svm_model.predict(df)
        lda_result = lda_model.predict(df)
        knn_result = knn_model.predict(df)
        df = {'SVM': [svm_result[0]], 'LDA': [lda_result[0]], 'KNN': [knn_result[0]]}
        df = pd.DataFrame(df)
    result = model.predict(df)[0]
    return result

class Predict(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        for prop in feature:
            parser.add_argument(prop)
        parser.add_argument('md')
        args = parser.parse_args()
        result = model_predict(args)
        return result, 200

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/result", methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        data_dict = request.form.to_dict()
        model_id = int(data_dict["md"])
        result = model_predict(data_dict)
        data_dict.pop('md',None)
        if result==0:
            conclude = "the patient does have a low probability of having CAD"
        else:
            conclude = "the patient does have a high probability of having CAD"
        annouced_result = models_name[model_id]+" model has predicted : " + conclude
        return render_template("result.html",data = data_dict, result=annouced_result)

API.add_resource(Predict, '/predict')

@app.route("/document")
def doc():
    return render_template("API.html")


    
if __name__ == "__main__":
    app.run(debug=True)

