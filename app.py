
from functions import *


# routes for the app to use the functions in functions.py to render the html pages and handle the requests from the
# user to the server and vice versa
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    return register()


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    return login()


@app.route('/logout')
def route_logout():
    return logout()


@app.route('/profile/<username>')
def route_profile(username):
    return profile(username)


@app.route('/feed')
def route_feed():
    return feed()


@app.route('/post', methods=['GET', 'POST'])
def route_post():
    return post()


@app.route('/comment', methods=['POST'])
def route_comment():
    return comment()


@app.route('/upvote_comment', methods=['POST'])
def route_upvote_comment():
    return upvote_comment()


@app.route('/downvote_comment', methods=['POST'])
def route_downvote_comment():
    return downvote_comment()


@app.route('/error')
def route_error():
    return error()


@app.route('/search')
def route_search():
    return search()


if __name__ == '__main__':
    app.run(debug=True)