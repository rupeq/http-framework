import json
from typing import Union, TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from http_framework import Response

JsonType: TypeAlias = Union[
    None, int, str, bool, list["JsonType"], dict[str, "JsonType"]
]


def jsonify(data: JsonType, status: int = 200) -> "Response":
    """
    Converts the given data into a JSON response.

    Args:
        data: The Python data structure to convert to JSON.
        status: The HTTP status code for the response.

    Returns:
        A `Response` object with the JSON data and appropriate headers.
    """

    json_body = json.dumps(data)
    from http_framework import Response

    return Response(json_body, status=status, content_type="application/json")
