from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle

df=pickle.load(open('df.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

def recommendation(song):
    idx= df[df['song']==song].index[0]
    distances=sorted(list(enumerate(similarity[idx])),reverse=False,key=lambda x:x[1])

    songs=[]
    for m_id in distances[1:21]:
        songs.append(df.iloc[m_id[0]].song)
    return songs 

app = Flask(__name__)

@app.route('/')
def index():
    names= list(df['song'].values)
    return render_template('index.html',name=names)

@app.route('/recom',methods=['POST'])
def ssong():
    user_song=request.form['names']
    
    if user_song == "":
        names = list(df['song'].values)
        return render_template('index.html', name=names)
    
    songs = recommendation(user_song)
    names= list(df['song'].values)
    context = {
        'name': names,
        'songs': songs,
        'user_song': user_song
    }
    return render_template('music-list.html', **context)


if __name__== "__main__":
    app.run(debug=True)