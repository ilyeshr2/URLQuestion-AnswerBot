from app import create_app
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

app = create_app()


CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

if __name__ == '__main__':
    app.run(debug=True)