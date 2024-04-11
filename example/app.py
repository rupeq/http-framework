from http_framework import HttpFramework, Blueprint, Request, Response
from http_framework.jsonify import jsonify

app = HttpFramework()

api = Blueprint("API Endpoints", prefix="/api/v1")


@api.route('/', methods=["GET"])
def index(request: Request) -> Response:
    return jsonify(
        {
            "message": "Hello World!",
            "query": request.query,
        }
    )


@api.route('/documents/<int:document_id>/versions/<version_id>', methods=["POST"])
def create_document(request: Request, document_id: int, version_id: str) -> Response:
    return jsonify(
        {
            "message": "Document created!",
            "id": document_id,
            "version_id": version_id,
            "body": request.json
        }
    )
