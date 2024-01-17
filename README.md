# `dragonfly`
dragonfly is a very simple Markdown-enabled paste service. It includes additional features such as self-destructing (deleted after being viewed) and custom identifiers for your pastes. The site is designed to be simple and easy to use. This project was made in about 2 hours 
as a demo for a friend who was interested in learning Python.
## `prerequisites`
In order to run dragonfly, you will need these Python packages:
```
pytz
python-dotenv
flask
flask_bootstrap
faunadb
gunicorn
mistletoe
```
After installing these packages, the Flask and Fauna secrets can be set in the `.env` file. A quick and easy way to generate a secret key for Flask can be done through secrets' "token_hex" function. Example:
```
Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import secrets
>>> secrets.token_hex(20)
'c3e9930ec882d024a79dd877e3e6496a01912048'
>>>
```
The secret for Fauna is located under the "security" tab in your database dashboard.
