from app import create_app   

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)