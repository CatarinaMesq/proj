import base64
import os
import sqlite3

from flask import render_template, request, redirect, url_for, session, flash, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

from forms import LoginForm

# Configs
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../proj/templates/assets'
app.secret_key = "my_secret_key"
csrf = CSRFProtect(app)

# Database connection
conn = sqlite3.connect('sarcastic_network.db', check_same_thread=False)
c = conn.cursor()


def register():
    # check if the request method is POST
    if request.method == 'POST':
        # get the username, email, and password from the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # validate the form inputs
        # check if any of the fields are empty
        if not username or not email or not password:
            return render_template('register.html', error='Please enter all fields')
        # check if any of the fields are less than 3 characters long
        if len(username) < 3 or len(email) < 3 or len(password) < 3:
            return render_template('register.html', error='Fields must be at least 3 characters long')

        # hash the password using sha256 encryption
        hashed_password = generate_password_hash(password, method='sha256')

        # check if the username or email already exists in the database
        c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        user = c.fetchone()
        if user:
            return render_template('register.html', error='Username or Email already exists')

        # insert the new user into the database
        c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, hashed_password))
        conn.commit()

        # redirect to the login page
        return redirect(url_for('route_login'))

    # if the request method is not POST, render the register template
    return render_template('register.html')


def login():
    # Create a new instance of the LoginForm class
    form = LoginForm()
    # Initialize the error variable to None
    error = None

    # If the request method is POST (meaning the user has submitted the form)
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Execute a SQL query to get the user with the given username
        c.execute("SELECT * FROM users WHERE username=?", (str(username),))
        conn.commit()
        # Fetch the first result of the query
        user = c.fetchone()

        # If a user was found with the given username
        if user:
            # Print the hashed password for debugging purposes
            print(user[3])
            # Check if the given password matches the hashed password in the database
            if check_password_hash(user[3], password):
                # If the passwords match, set the session variables and redirect to the index page
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                # If the passwords don't match, set the error variable and render the login template with the form and error message
                error = 'Incorrect Password'
                return render_template('login.html', form=form, error=error)
        else:
            # If no user was found with the given username, set the error variable and render the login template with the form and error message
            error = 'Username not found'
            return render_template('login.html', form=form, error=error)

    # If the request method is not POST, render the login template with the form and error (which will be None)
    return render_template('login.html', form=form, error=error)


def logout():
    session.pop('logged_in', None)  # remove the logged_in key from the session
    session.pop('username', None)  # remove the username key from the session
    return redirect(url_for('index'))  # redirect to the index page


def profile(username):
    form = LoginForm()

    # Retrieve user information from the database using the provided username
    c.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,))
    user = c.fetchone()

    # If no user was found, return an error message and HTTP status code 404
    if not user:
        return 'User not found', 404

    # Retrieve all posts made by the user and sort them by creation date, newest to oldest
    c.execute("""
        SELECT * FROM posts
        WHERE user_id = ?
        ORDER BY posts.created_at DESC
    """, (user[1],))
    posts = c.fetchall()

    # Retrieve all comments made by the user and sort them by timestamp, newest to oldest
    c.execute("""
            SELECT * FROM comments
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user[0],))
    comments = c.fetchall()

    post_list = []

    # Iterate through each post and create a dictionary containing relevant information
    for post in posts:
        # If the post content is a binary string, decode it and then encode it in base64 format
        if isinstance(post[2], bytes):
            encoded_string = base64.b64encode(post[2]).decode("utf-8")
        else:
            encoded_string = base64.b64encode(post[2].encode()).decode("utf-8")

        # Create a dictionary containing post information and append it to a list
        post_dict = {
            'id': post[0],
            'user_id': post[1],
            'picture': f"data:image/png;base64,{encoded_string}",
            'content': post[3],
            'created_at': post[4],
        }
        post_list.append(post_dict)

    # Render the user_profile.html template and pass in relevant information
    return render_template('user_profile.html', user=user, posts=post_list, comments=comments, form=form)


def feed():
    # Fetch all posts from the database and order them by creation date in descending order
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    # Fetch all comments from the database and order them by timestamp in descending order
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    # Create a new login form
    form = LoginForm()

    # Create an empty list to store the formatted posts and comments
    post_list = []

    # Iterate through each post
    for post in posts:
        # If the post image is a byte string, encode it as base64 and decode it to a utf-8 string.
        # Otherwise, encode the post image as utf-8 and then encode it as base64.
        if isinstance(post[2], bytes):
            encoded_string = base64.b64encode(post[2]).decode("utf-8")
        else:
            encoded_string = base64.b64encode(post[2].encode()).decode("utf-8")

        # Fetch all comments for this post from the database and order them by timestamp in descending order
        c.execute("""
            SELECT * FROM comments
            WHERE post_id = ?
            ORDER BY comments.timestamp DESC
        """, (post[0],))
        post_comments = c.fetchall()

        # Create an empty list to store the formatted comments for this post
        comment_list = []

        # Iterate through each comment for this post
        for comment in post_comments:
            # Create a dictionary to store the comment data
            comment_dict = {
                'id': comment[0],
                'user_id': comment[1],
                'post_id': comment[2],
                'content': comment[3],
                'timestamp': comment[4],
                'upvotes': comment[5]
            }
            # Append the formatted comment to the comment list for this post
            comment_list.append(comment_dict)

        # Create a dictionary to store the post data
        post_dict = {
            'id': post[0],
            'user_id': post[1],
            'picture': f"data:image/png;base64,{encoded_string}",
            'content': post[3],
            'created_at': post[4],
            'comments': comment_list
        }
        # Append the formatted post to the post list
        post_list.append(post_dict)

    # Render the feed template with the formatted posts, login form, and all comments
    return render_template('feed.html', posts=post_list, form=form, comments=comments)


# inserts a post on the feed page
def post():
    # Initialize the login form
    form = LoginForm()

    # Check if the user is logged in
    if 'username' not in session:
        flash('You must be logged in to post!', 'error')
        return redirect(url_for('route_login'))

    # Retrieve all posts and comments from the database
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    # If the request method is POST, the user has submitted a new post
    if request.method == 'POST':
        # Get the uploaded image
        image = request.files.get('image')

        # Check if the user uploaded an image
        if not image:
            flash('You must upload an image!', 'error')
            return redirect(request.url)

        # Check if the file is an image
        if not image.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            flash('Invalid file type. Please upload a JPG, JPEG, PNG, or GIF file.', 'error')
            return redirect(request.url)

        # Save the image to a temporary file
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Get the post content
        content = request.form['content']

        # Get the user ID of the logged-in user
        user_id = session['username']

        # Insert the post into the database
        with open(image_path, 'rb') as f:
            img_data = f.read()
        c.execute('INSERT INTO posts (user_id, picture, content) VALUES (?, ?, ?)', (user_id, img_data, content))
        conn.commit()

        # Delete the temporary file
        os.remove(image_path)

        # Retrieve all posts from the database
        c.execute("""
            SELECT * FROM posts
            ORDER BY posts.created_at DESC
        """)
        posts = c.fetchall()

        # Create a list of post dictionaries for rendering in the template
        post_list = []
        for post in posts:
            if isinstance(post[2], bytes):
                encoded_string = base64.b64encode(post[2]).decode("utf-8")
            else:
                encoded_string = base64.b64encode(post[2].encode()).decode("utf-8")
            post_dict = {
                'id': post[0],
                'user_id': post[1],
                'picture': f"data:image/png;base64,{encoded_string}",
                'content': post[3],
                'created_at': post[4]
            }
            post_list.append(post_dict)

        # Redirect the user to the feed page
        return redirect(url_for('route_feed'))

    # If the request method is not POST, redirect the user to the feed page
    return redirect(url_for('route_feed'))


def comment():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        # If not, redirect to the login page
        return redirect(url_for('route_login'))

    # Create a login form object
    form = LoginForm()

    # Get the ID of the post the comment is being added to
    post_id = request.form.get('post_id')

    # Get the user ID of the logged-in user
    user_id = session['username']

    # Get the content of the comment
    content = request.form.get('content')

    # Insert the comment into the database
    c.execute("""
        INSERT INTO comments (post_id, user_id, content, timestamp)
        VALUES (?,?,?,datetime('now'))
    """, (post_id, user_id, content))
    conn.commit()

    # Retrieve all posts from the database
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    # Retrieve all comments from the database
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    # Redirect the user to the feed page
    return redirect(url_for('route_feed'))


def upvote_comment():
    # Check if the user is logged in, and redirect to login page if not
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('route_login'))

    # Create a login form object
    form = LoginForm()

    # Get the comment ID from the request form
    comment_id = request.form.get('comment_id')

    # Update the comment's upvotes count in the database
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes + 1
        WHERE id = ?
    """, (comment_id,))
    conn.commit()

    # Get all the posts from the database and store them in the posts variable
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()

    # Get all the comments from the database and store them in the comments variable
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()

    # Redirect the user to the feed page
    return redirect(url_for('route_feed'))


def downvote_comment():
    # Check if user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('route_login'))

    # Get comment ID from form data
    comment_id = request.form.get('comment_id')

    # Decrement the upvote count for the comment in the database
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes - 1
        WHERE id = ?
    """, (comment_id,))

    # Commit changes to the database
    conn.commit()

    # Redirect to the feed page
    return redirect(url_for('route_feed'))


from flask import abort


def error():
    # Raise a 404 error page
    abort(404)


def search():
    # Get the user's search query from the URL query string
    query = request.args.get('q')

    # If there is no search query, redirect to the error page
    if not query:
        return redirect(url_for('error'))

    # Use the LIKE operator with wildcards to search for posts that contain the query string
    sql = "SELECT * FROM posts WHERE content LIKE ?"
    params = ('%' + query + '%',)
    c.execute(sql, params)
    posts = c.fetchall()

    # Prepare a list of dictionaries containing information about the posts found
    post_list = []
    for post in posts:
        # Convert the post picture to a base64 encoded string for display on the page
        if isinstance(post[2], bytes):
            encoded_string = base64.b64encode(post[2]).decode("utf-8")
        else:
            encoded_string = base64.b64encode(post[2].encode()).decode("utf-8")

        post_dict = {
            'id': post[0],
            'user_id': post[1],
            'picture': f"data:image/png;base64,{encoded_string}",
            'content': post[3],
            'created_at': post[4],
        }
        post_list.append(post_dict)

    # Render the search results page with the query and post list
    return render_template('search.html', query=query, posts=post_list)
