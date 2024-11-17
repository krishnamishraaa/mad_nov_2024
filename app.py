from backend import create_app
from flask import render_template
from flask_security import auth_required

app=create_app()

@app.route('/')
@auth_required("basic")
def index():
    print("Index route accessed")  # Add this line
    return "Hello, World!"

if __name__ == "__main__":
    app.run()

