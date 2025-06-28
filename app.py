from flask import Flask
from auth import auth_bp
from book import book_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)

@app.route("/")
def home():
    return {"message": "API Flask attiva"}

if __name__ == "__main__":
    app.run(debug=True)
