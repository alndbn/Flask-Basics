from flask import Flask, render_template
import json
from flask import Flask


app = Flask(__name__)


def load_posts():
    """opens the blogposts.json file and returns a list"""
    with open("blogposts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    """saves all blogposts in json file"""
    with open("blogposts.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    "Render the homepage with all blog posts"
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/')
def hello_world():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)