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

To check the version of python you can run the command

```python
4. which python
```

The project uses Flask as the micro-backend framework for building the backend and establishing the API. Let's install the [flask](https://flask.palletsprojects.com/en/2.1.x/) module.

```python
5. pip3 install flask
```

Once, you have installed the Flask module you are good to go with running the `app.py` file.

```python
6. python3 app.py
```
