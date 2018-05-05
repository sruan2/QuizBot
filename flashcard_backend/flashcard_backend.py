from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
        return 'Hello world'

    if __name__ == '__main__':
        context = ('/etc/letsencrypt/live/smartprimer.org/fullchain.pem', '/etc/letsencrypt/live/smartprimer.org/privkey.pem')
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
