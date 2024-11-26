from backend import create_app
from flask_security import auth_required

app=create_app()


@app.route('/')
@auth_required("basic")
def index():
    print("Index route accessed") 
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host= '127.0.0.1', port=5000, debug=True)

