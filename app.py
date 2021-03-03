# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Area = int(request.form['Area'])
        Area2 = np.log(Area)
        BHK = int(request.form['BHK'])
        Bathroom = int(request.form['Bathroom'])
        Status = request.form['Status']
        if(Status =='Ready to move'):
            Status = 1
        else:
            Status = 0
        Transaction = request.form['Transaction']    
        if(Transaction=='New Property'):
            Transaction = 0
        else:
            Transaction = 1
        Type = request.form['Type']    
        if(Type=='Apartment'):
            Type = 0
        else:
            Type = 1    

        prediction=model.predict([[Area2,BHK,Bathroom,Status,Transaction,Type]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Please input the valid value")
        else:
            return render_template('index.html',prediction_text="You Can Have the flat at {} INR approx".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
