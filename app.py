from flask import Flask
from view import PushingMessage
app = Flask(__name__)

app.register_blueprint(PushingMessage)


if __name__ == "__main__":
    app.run(debug=True)    