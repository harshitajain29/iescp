from flask import Flask, render_template, url_for

app = Flask(__name__, static_url_path='/static')
import config
import routes
import models

if __name__ == '__main__':
    app.run(debug=True)