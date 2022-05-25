<p align="center">
<img src="https://landen.imgix.net/2l01jamio2ce/assets/nzfrsbuc.png?w=1200&h=900&fit=max" height="120" width="120"/>
<h1 align="center">Stargazers</h1>
<p align="center">Building an endpoint that must return the list of neighbours repositories, meaning repositories where stargazers are found in common</p>
</p>

# Steps to run the project 🧑‍💻
We start with creating a virtual environment. With the initialization of the virtual environment, the installation of the modules becomes easy. 

Let's install the `virtualenv` module

```python
1. python3 -m pip install --user virtualenv
```

Once, we have the module install we need to create the environment. Over here, I am naming the environment to be `mergify` you are free to give it whatever you prefer.

```python
2. python3 -m venv mergify
```

When the above command is ran, the virtual environment gets created. Now, we activate the virtual environment

```python
3. source mergify/bin/activate
```

To check the path python you can run the command

```python
4. which python
```

The project uses Flask as the micro-backend framework for building the backend and establishing the API. Let's install the [flask](https://flask.palletsprojects.com/en/2.1.x/) module.

```python
5. pip3 install flask
```

Since, the versioning of modules correlated can vary, I would suggest you to install all the modules via `requirements.txt`
```python
6. pip install requirements.txt
```

Once, you have installed the Flask module you are good to go with running the `app.py` file.

```python
7. python3 lib/app.py
```

# Approach to build 💪
1. Initially we setup the Flask application with a simple home route. 
```python
from flask import Flask

# initializing the Flask application
app = Flask(__name__)

# home route
@app.route("/")
def index():
    return ("<h1>Hello, Stargazers from Mergify 👋</h1>")

if __name__ == "__main__":
    app.run(debug=True)
```

2. Once the home route is configured we focus on building the middleware. Over here, we actually need two middlewares:
- One to fetch all the users who have stared a particular repository
- One to fetch all the repositories started by a particular user

First thing first,
```python
def getUsersFromRepo(username:str,reponame:str):
    url = "https://api.github.com/repos/" + username + "/" + reponame +"/stargazers"
    with urlopen(url) as r:
        text = json.loads(r.read())
        stargazers = []
        for item in text:
            stargazers.append(item['login'])
    return stargazers
```
Over, here we use the GitHub API "https://api.github.com/repos/OWNER/REPO/stargazers" to fetch all the details of the users who stared a particular repository. After we have all the data stored in `text` object we destructure it and get only the usernames of the users as required. We append all the username in a list named `stargazers` and then return it. 

Secondly, 
```python
def getReposFromUser(username:str):
    url = "https://api.github.com/users/"+username+"/starred?per_page=10000" 
    with urlopen(url) as r:
        text = json.loads(r.read())
        repos=[]
        for item in text:
                repos.append(item['full_name'])
    return repos
```
Here, we use the GitHub API "https://api.github.com/users/USERNAME/starred" to get all the repositories stared by a single user. We get all the details with and count with a limit of 10,000 on the number of values we get. We store all the values in `text`. We destructure the text object and append only the `full_name` fields in a list known as repos and finally, return it.

3. Finally, we build the API end point. The basic algorithm which we follow to develop is written step by step:
The API end point which we built is: `/repos/<user>/<repo>/starneighbours`
- Step 1: Get all the stargazers for the repository sent in the request
- Step 2: Get each stargazers who the stared repository
- Step 3: All the repos we get of which were stared by the stargazers are our neighbouring repos
- Step 4: Now we start our traversing. For the first stargazer we create a hashmap with repo name as the key and usernames as a list of values. The traversal would go on subsequently to other stargazers if stargazer has a the same repository which they have stared together the stargazer would get appended else, a new key value pair would be created at the base. Ultimately, add the list to the base list of parent stargazers.

```python
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
```
Ultimately, we are done. To get the code in total checkout the `lib/app.py`, you are free to modify it according to your need. 

# Demo 💻
When we use the URL `http://127.0.0.1:5000/repos/Aniket762/playground/starneighbours` to get the data we get. 
<p align="center">
<img width="1440" alt="Data fetched from Playground StarNeighbours Mergify" src="https://user-images.githubusercontent.com/67703407/170259365-d03d324d-f961-4bef-a012-82547589d0fa.png">

</p>
Although,there are more data which comes along. But, for simplicity data which is enough to showcase the data structure is shown. 

# Scopes of improvement for the application 🤓
1. The current time complexity of the code is O(nm) where n is the number of stargazer and m is the number of repository. The time complexity of the program can be significantly improved with proper ananlysis.
2. Although, from a bird's eye the code may seem perfectly fine. In it's way of working, but there is no tests written to tackle the corner cases.
3. The application uses 2 External APIs in it's core to fetch data, even if one gets deprecated the application breaks with no particular message display. 




