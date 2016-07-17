from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# @app.route("/space",['PUT'])
# def create_space():
#     return None

if __name__ == "__main__":
    app.run(host='0.0.0.0')
