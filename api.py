from flask import Flask, request, send_from_directory, send_file
from flask_restful import Api
from controllers import urlUploadController
from controllers import convertUploadController
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_url_path='/')
CORS(app)

api = Api(app)

api.add_resource(urlUploadController.UrlUploadController, '/api/urlUpload')
api.add_resource(convertUploadController.ConvertUploadController, '/api/convertUpload')


@app.route('/layer/<path:id>')
def send_layer(id):
    return send_from_directory('/home/eran/Desktop/temp', id)

@app.route('/<path:path>')
def send_js(path):
    print(0)
    return send_from_directory('public', path)

@app.route('/')
def index():
    return send_file('public/index.html')

if __name__ == '__main__':
    app.run(debug=True)
