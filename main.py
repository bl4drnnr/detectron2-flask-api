import os

from flask import Flask
from flask_restful import Api

from src.detect_area_base64 import DetectAreaBase64
from src.detect_area_all import DetectAreaAll
from src.detect_area_by_name import DetectAreaByName

app = Flask(__name__)
api = Api(app)


@app.route('/api')
def main():
    return f'''
        <h1>The Flask App has been started on port {os.getenv('APPLICATION_PORT')} (container)</h1>
        <h1>Outside exposed port is {os.getenv('EXPOSE_PORT')}</h1>
    '''


api.add_resource(DetectAreaBase64, '/api/detect-area-base64')
api.add_resource(DetectAreaAll, '/api/detect-area-all')
api.add_resource(DetectAreaByName, '/api/detect-area-by-name')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('APPLICATION_PORT'), debug=True)
