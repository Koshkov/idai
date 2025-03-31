from flask import Flask, render_template
from flask_wtf import FlaskForm, CSRFProtect

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from forms.detect_form import AICheckForm
from forms.contribute_form import ContributeForm

import secrets, pickle, os, uuid
import numpy as np
import pandas as np

from settings import *

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to preprocess text
def _preprocess(text):
    text = str(text).lower()  # Convert to lowercase
    words = word_tokenize(text)  # Tokenize
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]  
    return " ".join(words)  

def _load():
    try:
        svm_binary = MODEL
        svm = open (svm_binary, "rb")
        model_svm = pickle.load(svm)
        svm.close()
        return model_svm
    except IOError:
        print(f"Failed to load {svm_binary}")

def _predict(model,text):
    text = _preprocess(text)
    res = model.predict_proba([text])
    res = {"human":f"{res[0][0]*100:.2f}","ai": f"{res[0][1]*100:.2f}" }
    return res

app = Flask(__name__)
key = secrets.token_urlsafe(16)
app.secret_key = key
csrf = CSRFProtect(app)
svm = _load()

@app.route('/about')
def about():
    return render_template("/about.html");

@app.route('/contribute',methods=['GET','POST'])
def contribute():
    form = ContributeForm()
    message=""
    if form.validate_on_submit():
        essay = form.text.data
        ai_status = form.ai_status.data
        uid = uuid.uuid4()
        try:
            log=open(f'{CONTRIBS}/contribs_{uid}.csv','w')
            log.write(f"{uid}\n{ai_status}\n{essay}")
            message = f"Thank you! Your sumission id is: {uid}"
            log.close()
        except IOError:
            print(f"Failed")
            message=f"Submission failed!"

    return render_template("/contribute.html",form=form,message=message);

@app.route('/',methods=['GET','POST'])
def home():
    form  = AICheckForm()
    message=""
    if form.validate_on_submit():
        essay = form.text.data
        message = _predict(svm,essay)
    return render_template("/home.html",form=form, message=message);

if __name__ == '__main__':
    app.run(debug=True)
