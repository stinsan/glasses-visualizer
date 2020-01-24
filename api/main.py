from flask import Flask
from flask_restful import reqparse, Resource, Api
from werkzeug import datastructures
import werkzeug
import base64

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    #  Just a basic hello world as the root endpoint ('\').
    #  want to keep this here just cause.
    def get(self):
        return {'hello': 'world'}


class Upload(Resource):

    #  POST method for uploading images. The endpoint is \upload.
    #  At this moment, it just spits out a JSON with the encoded image string.
    #  How to cURL: curl http://your-server/upload -F "image=@your-image.jpg".

    def post(self):
        parser = reqparse.RequestParser()  # Initialize the parser.
        parser.add_argument('image',       # Add 'image' as an argument of type FileStorage.
                            type=werkzeug.datastructures.FileStorage,
                            location='files')
        args = parser.parse_args()         # Get the arguments by parsing.

        image = args['image']                           # Get the image from the 'image' argument.
        encoded_image = base64.b64encode(image.read())  # Encode the image in base 64 so we can stick in a JSON object.
        # The read() function turns the image (originally of type FileStorage) into a byte stream so it can be encoded.

        # Return the JSON object containing the base 64 encoding of the image.
        # We must explicitly turn it into a string because it is originally of type bytes,
        # and bytes are not JSON serializable.
        return {'image_base64': str(encoded_image, 'utf-8')}


# Add the endpoints.
api.add_resource(HelloWorld, '/')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
