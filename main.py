from flask_wtf.csrf import CSRFProtect
from app import app

app.secret_key = "my_secret_key"
csrf = CSRFProtect(app)

if __name__ == '__main__':
    app.run(debug=True)
