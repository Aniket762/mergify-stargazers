from flask import Flask, jsonify, make_response,json
from urllib.request import urlopen 

# initializing the Flask application
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Middlewares

# Text: Payload, wherever text is mentioned I meant payload

## Get all the users who stared the repo
def getUsersFromRepo(username:str,reponame:str):
    # in the particular URL we pass in username and reponame as the parameter 
    url = "https://api.github.com/repos/" + username + "/" + reponame +"/stargazers"
    # we open the url as variable r
    with urlopen(url) as r:
        # we read from the variable r and converts in json format
        text = json.loads(r.read())
        # we define an empty list 
        stargazers = []
        # we parse over every item in the text
        for item in text:
            # from the item we destructure and append only the value corresponding
            # to login, thus our repos list gets filled in with data
            stargazers.append(item['login'])
    return stargazers

##  Get all the repos stared by a user
def getReposFromUser(username:str):
    # in the particular URL we pass in username as the parameter 
    # the per_page variable shows the maximum threshold of 10000
    url = "https://api.github.com/users/"+username+"/starred?per_page=10000" 
    # we open the url as variable r
    with urlopen(url) as r:
        # we read from the variable r and converts in json format
        text = json.loads(r.read())
        # we define an empty list 
        repos=[]
        # we parse over every item in the text
        for item in text:
                # from the item we destructure and append only the value corresponding
                # to full_name, thus our repos list gets filled in with data
                repos.append(item['full_name'])
    return repos

# home route
@app.route("/")
def index():
    return ("<h1>Hello, Stargazers from Mergify 👋</h1>")

# master route
@app.route("/repos/<string:username>/<string:reponame>/starneighbours",methods = ['GET'])
def getStarNeighbours(username:str,reponame:str):
    # getting all the users who stared the repo passed in as parameter
    stargazers =  getUsersFromRepo(username,reponame)
    # defining a dict 
    resultant={}
    # parsing every stargazer from the list of stargazers
    for stargazer in stargazers:
        # for every stargazer we get all the repos he/she stared 
        allRepos= getReposFromUser(stargazer)
        # we parse over every repo
        for repo in allRepos:
            # if the resultant dict doesn't contain the following repo as the key
            # a new key value pair would gets created
            if repo not in resultant:
                resultant[repo]=[stargazer]
            else:
            # if the repo is already present as the key, the new stargazer gets appended
                resultant[repo].append(stargazer)
    # ultimately, we convert into JSON and return 
    return jsonify(resultant)

if __name__ == "__main__":
    app.run(debug=True)