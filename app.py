from flask import Flask, render_template, request, redirect, url_for, session
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with your own secret key

# Sample user data (in a real application, this would be stored securely)
users = {
    "user1": {"email": "user1@example.com", "password": "password1"},
    "user2": {"email": "user2@example.com", "password": "password2"}
}

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Load the TF-IDF vectorizer
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')


@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/portal')
def portal():
    if 'username' in session:
        return render_template('portal.html')
    else:
        return redirect(url_for('index', error=True))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username and password match a user in the database
    if username in users and users[username]['password'] == password:
        # Store the username in the session
        session['username'] = username
        # Redirect to the portal page upon successful login
        return redirect(url_for('portal'))
    else:
        # Redirect back to the login page with an error message
        return redirect(url_for('index', error=True))

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'username' in session:
        review = request.form['review']
        # Perform text preprocessing (e.g., tokenization, stop word removal)
        processed_review = preprocess(review)
        # Vectorize the review using the TF-IDF vectorizer
        vectorized_review = tfidf_vectorizer.transform([processed_review])
        # Predict the sentiment of the review using the trained model
        sentiment_prediction = best_rf_model.predict(vectorized_review)
        # Render the template with the prediction result
        return render_template('analysis_result.html', review=review, sentiment=sentiment_prediction[0])
    else:
        return redirect(url_for('index', error=True))

def preprocess(text):
    # Implement your text preprocessing steps here
    return text

if __name__ == '__main__':
    app.run(debug=True)
