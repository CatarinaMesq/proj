from flask import Flask
from functions import *

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for registering a new user
@app.route('/register', methods=['GET', 'POST'])
def route_register():
    return register()

# Route for logging in an existing user
@app.route('/login', methods=['GET', 'POST'])
def route_login():
    return login()

# Route for logging out the current user
@app.route('/logout')
def route_logout():
    return logout()

# Route for displaying the profile of a user
@app.route('/profile/<username>')
def route_profile(username):
    return profile(username)

# Route for displaying the user's feed
@app.route('/feed')
def route_feed():
    return feed()

# Route for creating a new post
@app.route('/post', methods=['GET', 'POST'])
def route_post():
    return post()

# Route for adding a new comment to a post
@app.route('/comment', methods=['POST'])
def route_comment():
    return comment()

# Route for upvoting a comment
@app.route('/upvote_comment', methods=['POST'])
def route_upvote_comment():
    return upvote_comment()

# Route for downvoting a comment
@app.route('/downvote_comment', methods=['POST'])
def route_downvote_comment():
    return downvote_comment()

# Route for displaying the error page
@app.route('/error')
def route_error():
    return error()

# Route for performing a search
@app.route('/search')
def route_search():
    return search()

if __name__ == '__main__':
    app.run()
