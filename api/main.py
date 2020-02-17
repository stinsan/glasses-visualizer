from flask import Flask
from flask_restful import reqparse, Resource, Api
from werkzeug import datastructures
from monodepth2.test_simple import monodepth  # Local module import.

import werkzeug
import base64

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    """ Just a basic hello world as the root endpoint ('\').
    I want to keep this here for debugging purposes.
    """
    def get(self): 
        return {'hello': 'world'}


class Upload(Resource):
    """ POST method for uploading images. The endpoint is \upload.
    Returns the depth map given by Monodepth for the input image.
    How to cURL: curl http://your-server/upload -F "image=@your-image.jpg".
    """
    def post(self):
        parser = reqparse.RequestParser()  # Initialize the parser.
        parser.add_argument('image',       # Add 'image' as an argument of type FileStorage.
                            type=werkzeug.datastructures.FileStorage,
                            location='files')
        args = parser.parse_args()         # Get the arguments by parsing.
        image = args['image']              # Get the image from the 'image' argument.

        # Run Monodepth on the image, returns a bytes object.
        depth_map = monodepth(image)

        encoded_image = base64.b64encode(depth_map)  # Encode the image in base 64 so we can stick in a JSON object.

        # Return the JSON object containing the base 64 encoding of the image.
        # We must explicitly turn it into a string because it is originally of type bytes,
        # and bytes are not JSON serializable.
        return {'image': str(encoded_image, 'utf-8')}


# Add the endpoints.
api.add_resource(HelloWorld, '/')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
