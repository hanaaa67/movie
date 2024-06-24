from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# Establish MongoDB connection
client = MongoClient('mongodb+srv://aghnq:Faqih2006@cluster0.sepvmlq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    # Receive data from POST request
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    # Request data from the provided URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        
    response = requests.get(url_receive, headers=headers)
        
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract Open Graph meta tags
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')   

    image = og_image['content'] if og_image else ''
    title = og_title['content'] if og_title else ''
    desc = og_description['content'] if og_description else ''

    # Create document to insert into MongoDB
    doc = {
        'image': image,
        'title': title,
        'description': desc,
        'star': int(star_receive),
        'comment': comment_receive
    }

    # Insert document into MongoDB collection
    db.movies.insert_one(doc)
    return jsonify({'msg': 'POST request successful!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    # Retrieve all movies from MongoDB collection
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
