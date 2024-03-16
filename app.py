from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

import joblib

app = Flask(__name__)

best_rf_model = joblib.load('best_rf_model.pkl')

tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portal', methods=['GET', 'POST'])
def portal():
    if request.method== 'POST':
        return render_template('portal.html')
    else:
        return render_template('portal.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        phone_no = request.form.get('phone_no')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
    return render_template("sign.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    review = request.form['review']
    rating = int(request.form['rating']) 
    processed_review = preprocess(review)

    vectorized_review = tfidf_vectorizer.transform([processed_review])

    sentiment_prediction = best_rf_model.predict(vectorized_review)
    
    return render_template('analysis_result.html', review=review, rating=rating, sentiment=sentiment_prediction[0])


def preprocess(text):
    # Implement your text preprocessing steps here
    return text

if __name__ == '__main__':
    app.run(debug=True)