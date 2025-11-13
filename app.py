from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def load_posts():
    """opens the blogposts.json file and returns a list"""
    with open("blogposts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    """saves all blogposts in json file"""
    with open("blogposts.json", "w") as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    """Return a single post dictionary by ID, or None if not found."""
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    "Render the homepage with all blog posts"
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Show a form to add a new blog post or handle form submission."""
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()

        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
        }

        posts.append(new_post)

        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    """Delete a blog post with the given ID and redirect to homepage."""
    posts = load_posts()

    posts = [p for p in posts if p["id"] != post_id]

    save_posts(posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Update an existing blog post."""

    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        new_author = request.form.get("author")
        new_title = request.form.get("title")
        new_content = request.form.get("content")

        posts = load_posts()

        for p in posts:
            if p["id"] == post_id:
                p["author"] = new_author
                p["title"] = new_title
                p["content"] = new_content


        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)