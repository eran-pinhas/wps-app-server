from flask_restful import Resource, reqparse, request
import urllib
import storage

parser = reqparse.RequestParser()
parser.add_argument('key1', type=str)


class UrlUploadController(Resource):

    def post(self):
        json = request.get_json(force=True)
        url = json['url']
        stream = urllib.request.urlopen(url)
        print(type(stream))
        id = storage.add_file(stream)
        return {"id": id}
