from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['POST'])  # This request will be understood by our app
def home():
    return "Hello World!!"


if __name__ == '__main__':
    app.run(port=5000)