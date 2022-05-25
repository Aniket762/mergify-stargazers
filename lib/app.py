from flask import Flask, jsonify, make_response,json
from urllib.request import urlopen 

# initializing the Flask application
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Middlewares

## Get all the users who stared the repo
def getUsersFromRepo(username:str,reponame:str):
    url = "https://api.github.com/repos/" + username + "/" + reponame +"/stargazers"
    with urlopen(url) as r:
        text = json.loads(r.read())
        stargazers = []
        for item in text:
            stargazers.append(item['login'])
    return stargazers

##  Get all the repos stared by a user
def getReposFromUser(username:str):
    url = "https://api.github.com/users/"+username+"/starred?per_page=10000" 
    with urlopen(url) as r:
        text = json.loads(r.read())
        repos=[]
        for item in text:
                repos.append(item['full_name'])
    return repos

# home route
@app.route("/")
def index():
    return ("<h1>Hello, Stargazers from Mergify 👋</h1>")

# master route
@app.route("/repos/<string:username>/<string:reponame>/starneighbours",methods = ['GET'])
def getStarNeighbours(username:str,reponame:str):
    stargazers =  getUsersFromRepo(username,reponame)
    resultant={}
    for stargazer in stargazers:
        allRepos= getReposFromUser(stargazer)
        for repo in allRepos:
            if repo not in resultant:
                resultant[repo]=[stargazer]
            else:
                resultant[repo].append(stargazer)
    return jsonify(resultant)

if __name__ == "__main__":
    app.run(debug=True)