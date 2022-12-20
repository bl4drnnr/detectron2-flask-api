from src.detect_area_base64 import DetectAreaBase64
from src.detect_area_all import DetectAreaAll
from src.detect_area_by_name import DetectAreaByName

PORT = 5000

app = Flask(__name__)
api = Api(app)


@app.route('/api')
def main():
    return f'<h1>The Flask App has been started on port {PORT}</h1>'


api.add_resource(DetectAreaBase64, '/detect-area-base64')
api.add_resource(DetectAreaAll, '/detect-area-all')
api.add_resource(DetectAreaByName, '/detect-area-by-name')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
