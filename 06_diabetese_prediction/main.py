from flask import Flask, render_template, request 
import pickle 
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import Pipeline 

app = Flask(__name__, template_folder='templates')
svm_model = pickle.load(open('svm_model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')

def std_scalar(df):
    std_X = StandardScaler()
    x = pd.DataFrame(std_X.fit_transform(df))
    return x 


def pipeline(features):
    steps = [('scaler', StandardScaler()), ('SVM', svm_model)]
    pipe = Pipeline(steps) 
    return pipe.fit_transform(features) 



@app.route('/send', methods=['POST'])
def getdata():

    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]



    # Feature transform and prediction using pipeline 

    # We cna now use predictions from this feature_transformed variable  
    # feature_transformed = pipeline(final_features)  
                             
    feature_transform = std_scalar(final_features) 
    # Using standard scalar method 
    prediction = svm_model.predict(feature_transform)

    if prediction == 0:
        result = "You Are Non-Diabetic"
    else:
        result="You Are Diabetic" 

    Pregnancies = request.form['Pregnancies']
    Glucose = request.form['Glucose']
    Age = (request.form['Age'])
    BMI = (request.form['BMI'])
    BloodPressure = (request.form['BloodPressure'])
    SkinThickness = request.form['SkinThickness']
    Insulin = request.form['Insulin']
    DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']

    return render_template('show.html', preg=Pregnancies, bp=BloodPressure, age=Age, gluc=Glucose, bmi=BMI,
                            st=SkinThickness, ins=Insulin, dpf=DiabetesPedigreeFunction, res=result)




if __name__ == '__main__':
    app.run(debug=True)
