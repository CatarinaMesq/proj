import base64
import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import models
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'secret_key'  # a secret key is required for sessions
CSRFProtect(app)
app.config['UPLOAD_FOLDER'] = '../proj/templates/assets'

conn = sqlite3.connect('../sarcastic_network.db', check_same_thread=False)
c = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # validate inputs
        if not username or not email or not password:
            return render_template('register.html', error='Please enter all fields')
        if len(username) < 3 or len(email) < 3 or len(password) < 3:
            return render_template('register.html', error='Fields must be at least 3 characters long')

        hashed_password = generate_password_hash(password, method='sha256')

        c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        user = c.fetchone()
        if user:
            return render_template('register.html', error='Username or Email already exists')

        c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (username, email, hashed_password))
        conn.commit()
        # conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        c.execute("SELECT * FROM users WHERE username=?", (str(username),))
        conn.commit()
        user = c.fetchone()
        if user:

            print(user[3])
            if check_password_hash(user[3], password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = 'Incorrect Password'
                return render_template('login.html', form=form, error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/profile/<username>')
def profile(username):
    form = LoginForm()
    c.execute("""
        SELECT * FROM users
        WHERE username = ?
    """, (username,))
    user = c.fetchone()
    if not user:
        return 'User not found', 404
    print(user)
    c.execute("""
        SELECT * FROM posts
        WHERE user_id = ?
        ORDER BY posts.created_at DESC
    """, (user[1],))
    posts = c.fetchall()
    c.execute("""
            SELECT * FROM comments
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user[0],))
    comments = c.fetchall()

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
            'created_at': post[4],
        }
        post_list.append(post_dict)
    return render_template('user_profile.html', user=user, posts=post_list, comments=comments, form=form)


# the main page
@app.route('/feed')
def feed():
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
    form = LoginForm()
    post_list = []
    for post in posts:
        if isinstance(post[2], bytes):
            encoded_string = base64.b64encode(post[2]).decode("utf-8")
        else:
            encoded_string = base64.b64encode(post[2].encode()).decode("utf-8")
        c.execute("""
            SELECT * FROM comments
            WHERE post_id = ?
            ORDER BY comments.timestamp DESC
        """, (post[0],))
        post_comments = c.fetchall()
        comment_list = []
        for comment in post_comments:
            comment_dict = {
                'id': comment[0],
                'user_id': comment[1],
                'post_id': comment[2],
                'content': comment[3],
                'timestamp': comment[4],
                'upvotes': comment[5]
            }
            comment_list.append(comment_dict)
        post_dict = {
            'id': post[0],
            'user_id': post[1],
            'picture': f"data:image/png;base64,{encoded_string}",
            'content': post[3],
            'created_at': post[4],
            'comments': comment_list
        }
        post_list.append(post_dict)
    return render_template('feed.html', posts=post_list, form=form, comments=comments)


# inserts a post on the feed page
@app.route('/post', methods=['GET', 'POST'])
def post():
    form = LoginForm()
    if 'username' not in session:
        flash('You must be logged in to post!', 'error')
        return redirect(url_for('login'))

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

        os.remove(image_path)

        c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
        """)
        posts = c.fetchall()

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

        return redirect(url_for('feed'))

    return redirect(url_for('feed'))


@app.route('/comment', methods=['POST'])
def comment():
    form = LoginForm()
    post_id = request.form.get('post_id')
    user_id = session['username']
    content = request.form.get('content')
    c.execute("""
        INSERT INTO comments (post_id, user_id, content, timestamp)
        VALUES (?,?,?,datetime('now'))
    """, (post_id, user_id, content))
    conn.commit()

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

    return redirect(url_for('feed'))


@app.route('/upvote_comment', methods=['POST'])
def upvote_comment():
    form = LoginForm()
    comment_id = request.form.get('comment_id')
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes + 1
        WHERE id = ?
    """, (comment_id,))

    conn.commit()
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

    return redirect(url_for('feed'))


@app.route('/downvote_comment', methods=['POST'])
def downvote_comment():
    comment_id = request.form.get('comment_id')
    c.execute("""
        UPDATE comments
        SET upvotes = upvotes - 1
        WHERE id = ?
    """, (comment_id,))
    conn.commit()
    return redirect(url_for('feed'))


from flask import abort


@app.route('/error')
def error():
    abort(404)


@app.route('/search')
def search():
    query = request.args.get('q')  # Get the user's search query from the URL query string
    if not query:
        return redirect(url_for('error'))

    # Use the LIKE operator with wildcards to search for posts that contain the query string
    sql = "SELECT * FROM posts WHERE content LIKE ?"
    params = ('%' + query + '%',)
    c.execute(sql, params)
    posts = c.fetchall()

    post_list=[]
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
            'created_at': post[4],
        }
        post_list.append(post_dict)
    return render_template('search.html', query=query, posts=post_list)


if __name__ == '__main__':
    models.init_db()
    app.run(debug=True, port=8083)
