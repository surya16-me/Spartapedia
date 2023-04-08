from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

client = MongoClient('mongodb+srv://surya:surya@cluster0.ovgnl6x.mongodb.net/?retryWrites=true&w=majority')
db = client.dbadmin

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_rec = request.form['url_in']
    star_rec = request.form['star_in']
    comment_rec = request.form['comment_in']
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_rec,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    desc = og_description['content']

    doc = {
        'image' : image,
        'title' : title,
        'description' : desc,
        'star' : star_rec,
        'comment' : comment_rec
    }

    db.movie_list.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movie_list.find({},{'_id':False}))
    return jsonify({'movies':movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)