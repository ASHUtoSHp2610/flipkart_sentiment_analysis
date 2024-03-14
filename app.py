from flask import Flask, render_template, request, redirect, url_for, session

import joblib

app = Flask(__name__)

best_rf_model = joblib.load('best_rf_model.pkl')

tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')


@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/portal')
def portal():
        return render_template('portal.html')

@app.route('/login', methods=['POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup')
def sign():
    return render_template('sign.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'username' in session:
        review = request.form['review']
        rating = int(request.form['rating'])  # Convert rating to integer
        # Perform text preprocessing (e.g., tokenization, stop word removal)
        processed_review = preprocess(review)
        # Vectorize the review using the TF-IDF vectorizer
        vectorized_review = tfidf_vectorizer.transform([processed_review])
        # Predict the sentiment of the review using the trained model
        sentiment_prediction = best_rf_model.predict(vectorized_review)
        # Render the template with the prediction result
        return render_template('analysis_result.html', review=review, rating=rating, sentiment=sentiment_prediction[0])
    else:
        return redirect(url_for('index', error=True))


def preprocess(text):
    # Implement your text preprocessing steps here
    return text

if __name__ == '__main__':
    app.run(debug=True)
