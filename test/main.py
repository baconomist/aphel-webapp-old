from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/")
@app.route("/<user>")
def index(user=None):
    return render_template("user.html", user=user)

@app.route("/shopping")
def shopping():
    shopping_list = ["cheese", "tuna", "beef"]
    return render_template("shopping.html", shopping_list=shopping_list)

'''
@app.route("/bacon", methods=["GET", "POST"])
def bacon():
    if request.method == "GET":
        return "You are using GET"
    elif request.method == "POST":
        return "You are using POST"

@app.route("/profile/<username>")
def profile(user):
    return render_template("profile.html", user=user)

@app.route("/post/<int:post_id>")
def post(post_id: int):
    return "<h2> Post %s</h2>" % post_id
'''

if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)