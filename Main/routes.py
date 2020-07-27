from flask import render_template, request, url_for, redirect
from Main import app
from playsound import playsound
import random
import heapq
topPerformers=[]
heapq.heapify(topPerformers)
class PQNode:
    def __init__(self,playerName,score):
        self.playerName=playerName
        self.score=score
    
    def __lt__(self,other):
        return self.score < other.score
    
    def __str__(self):
        return str("{} : {}".format(self.playerName,self.score))
def scorebard_calculation(playerName,score):
    item=PQNode(playerName,score)
    if(len(topPerformers)<10):
        heapq.heappush(topPerformers,item)
    else:
        temp=topPerformers[0]
        if(temp.score<item.score):
            heapq.heappop(topPerformers)
            heapq.heappush(topPerformers,item)
        
    




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/name-collection")
def name():
    return render_template('name-collection.html')

audios={
    'example.mp3':"a thing characteristic of its kind or illustrating a general rule.",
    'hello.mp3':"used as a greeting or to begin a telephone conversation.",
    'science.mp3':"a systematically organized body of knowledge on a particular subject.",
    'world.mp3':"the earth, together with all of its countries and peoples.",
}
score=0
key=""
val=""
def restart():
    score=0


@app.route("/game-start",methods=['POST'])
def play():
    playerName=request.form.get("player-name")
    score=request.form.get("score")
    key,val=randomAudioGenerator()
    print(key,val)
   
    return render_template('game-started.html',name=playerName,score=score,key=key,val=val)
    
def randomAudioGenerator():
    key, val = random.choice(list(audios.items()))
    return (key,val)

#isplaying=False
@app.route("/play-word",methods=['POST'])
def playing():
    key=request.form.get("key")
    val=request.form.get("val")
    playerName=request.form.get("player-name")
    score=request.form.get("score")
    print(key,val)
    playsound('Main/static/audio/'+key)
    return render_template('game-started.html',name=playerName,score=score,key=key,val=val)
    

#validatng
@app.route("/checkit",methods=['POST'])
def checking():
    key=request.form.get("key")
    val=request.form.get("val")
    userval=request.form.get("guess-word")
    playerName=request.form.get("player-name")
    score=request.form.get("score")
    print(key,val,userval,int(score)+1)
    if(key[:-4].lower()==userval.lower()):
        #render_template('game-started.html',name=playerName,score=score+1,)
        print("ok")
        score=int(score)+1
        return render_template('correct.html',name=playerName,score=score)
    else:
        scorebard_calculation(playerName,score)
        #print(topPerformers)
        return render_template('incorrect.html',name=playerName,score=0)


@app.route("/leaderboard")
def leaderboardDisplay():
    return render_template('leaderboard-view.html',topPerformers=sorted(topPerformers,reverse=True))

     
    




    

