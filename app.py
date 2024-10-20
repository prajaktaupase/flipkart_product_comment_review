from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

app = Flask(__name__)
app.static_folder = 'static'

def analyze_sentiment(text):
    sentiment_score = TextBlob(text).sentiment.polarity
    if sentiment_score > 0.3:
        return 'Positive'
    elif sentiment_score < -0.2:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ul')
def ul():
    return render_template('ul.html')

@app.route('/anal', methods=['POST'])
def anal():
    if request.method == 'POST':
        url = request.form['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('div', {'class': 'ZmyHeo'})
        reviews_data = []
        total_sentiment_score = 0
        total_reviews = 0
        analyzed_reviews = []
        reviews_for_url = []
        for review in reviews[:25]:
            text = review.text
            text = ' '.join(text.split())
            text = ''.join(e for e in text if e.isalnum() or e.isspace())
            sentiment_score = TextBlob(text).sentiment.polarity
            total_sentiment_score += sentiment_score
            total_reviews += 1
            sentiment = ""
            if sentiment_score > 0.3:
                sentiment = "Positive"
            elif sentiment_score < 0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            reviews_for_url.append({'text': text, 'sentiment': sentiment})
        reviews_data.append({'url': url, 'reviews': reviews_for_url})
        if total_reviews != 0:
            average_sentiment_score = total_sentiment_score / total_reviews
        else:
            average_sentiment_score = 0
        return render_template('anal.html', reviews_data=reviews_data, average_sentiment_score=average_sentiment_score)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Testing')
def Testing():
    return render_template('Testing.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    sentiment = analyze_sentiment(text)
    return render_template('result.html', text=text, sentiment=sentiment)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
