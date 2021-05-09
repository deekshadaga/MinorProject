from flask import Flask, render_template, request, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytube import YouTube
import video
import playlist
import audio
import re
from datetime import date

app = Flask(__name__)
app.secret_key = '\xc6g\x905\x96?\xeek\xe8_h_'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ytextractor.db"
app.config['SQLALCHEMY_BINDS']={'history':'sqlite:///history.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ytextractor(db.Model):
    uname = db.Column(db.String(200),primary_key=True)
    passwd = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    def __repr__(self)->str:
        return f"{self.uname} - {self.passwd} - {self.email}"

class history(db.Model):
    __bind_key__='history'
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200),nullable=False)
    title = db.Column(db.String(200), nullable=False)
    typeof = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=date.today)

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/aboutl', methods=['GET', 'POST'])
def aboutl():
    username=request.args.get('username')
    return render_template('aboutl.html',username=username)

@app.route('/audio_download', methods=['GET', 'POST'])
def audio_download():
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        audio.audiodownload(url)
    return render_template('audio.html')

@app.route('/video_download', methods=['GET', 'POST'])
def video_download():
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        video.videodownload(url)
    return render_template('video.html')

@app.route('/playlist_download', methods=['GET', 'POST'])
def playlist_download():
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        playlist.playlistdownload(url)
    return render_template('playlist.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        query =  db.session.query(ytextractor).filter(ytextractor.uname.in_([username]), ytextractor.passwd.in_([password]))
        account = query.first()
        if account:
            return render_template('indexl.html',username=username)
        else:
            flash('Incorrect username / password !')
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('/'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        emailid = request.form['email']
        account = db.session.query(ytextractor.uname).filter_by(uname=username).first()
        if account:
            flash('Account already exists !')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            flash('Invalid email address !')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers !')
        elif not username or not password or not emailid:
            flash('Please fill out the form !')
        else:
            yte=ytextractor(uname=username,passwd=password,email=emailid)
            db.session.add(yte)
            db.session.commit()
            return render_template('indexl.html',username=username)
    elif request.method == 'POST':
        flash('Please fill out the form !')
    return render_template('register.html')

@app.route('/delete/<int:sno>')
def delhis(sno):
    his = history.query.filter_by(sno=sno).first()
    username = his.uname
    db.session.delete(his)
    db.session.commit()
    path="http://127.0.0.1:5000/history?username="+username
    return redirect(path)
    
@app.route('/indexl', methods=['GET', 'POST'])
def indexl():
    username=request.args.get('username')
    return render_template('indexl.html',username=username)

@app.route('/audiol', methods=['GET', 'POST'])
def audiol():
    username=request.args.get('username')
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        audio.audiodownload(url)
        his=history(uname=username,title=url,typeof='Audio')
        db.session.add(his)
        db.session.commit()
    return render_template('audiol.html',username=username)

@app.route('/videol', methods=['GET', 'POST'])
def videol():
    username=request.args.get('username')
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        video.videodownload(url)
        his=history(uname=username,title=url,typeof='Video')
        db.session.add(his)
        db.session.commit()
    return render_template('videol.html',username=username)

@app.route('/playlistl', methods=['GET', 'POST'])
def playlistl():
    username=request.args.get('username')
    if request.method=='POST':
        url = request.form['url']
        if not url.startswith('http'):
            url='https://'+url
        playlist.playlistdownload(url)
        his=history(uname=username,title=url,typeof='Playlist')
        db.session.add(his)
        db.session.commit()
    return render_template('playlistl.html',username=username)

@app.route('/history', methods =['GET', 'POST'])
def his():
    username=request.args.get('username')
    allhistory = history.query.filter_by(uname=username).all()
    return render_template('history.html',username=username,allhistory=allhistory)


if __name__ == "__main__":
    app.run(debug=True, port=5000)