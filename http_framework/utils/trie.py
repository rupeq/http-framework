from collections import OrderedDict
from typing import Optional, Callable, Any

HandlerType = Callable[..., Any]


class TrieNode:
    """A node in the trie structure for storing route handlers."""

    def __init__(self):
        self.children: dict[str, TrieNode] = OrderedDict()
        self.handlers: dict[str, Callable] = OrderedDict()


class Trie:
    """Trie data structure for efficient route matching and insertion."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, path_parts: list[str], method: str, handler: HandlerType) -> None:
        """
        Inserts a handler for the given path parts into the trie.

        Parameters:
            - path_parts: A list of segments from a split URL path.
            - handler: A callable that handles the request for the route.
        """
        node = self.root
        for part in path_parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.handlers[method.upper()] = handler

    @staticmethod
    def convert_param_to_type(param_value: str, param_type: str | None = None) -> Any:
        """
        Converts a parameter value to the specified type.

        Parameters:
            - param_value: The value of the parameter.
            - param_type: The type of the parameter.

        Returns:
            The converted value.

        Raises:
            TypeError: If the parameter type is not supported.
        """

        if param_type == "int":
            return int(param_value)
        elif param_type == "float":
            return float(param_value)
        elif param_type == "str":
            return str(param_value)
        elif param_type == "bool":
            return bool(param_value)

        raise TypeError("Unsupported type.")

    def match(
        self, path_parts: list[str], method: str
    ) -> tuple[Optional[HandlerType], dict[str, str]]:
        """
        Attempts to find a handler for the given path parts. Supports dynamic routing.

        Parameters:
            - path_parts: A list of segments from a split URL path.

        Returns:
            A tuple of the found handler (or None if not found) and a dictionary of path parameters.
        """
        node = self.root
        params = {}
        for idx, part in enumerate(path_parts):
            if idx == len(path_parts) - 1 and "?" in part:
                part, _ = part.split("?")

            if part in node.children:
                node = node.children[part]

            elif dynamic_part := next(
                filter(lambda x: x.startswith("<"), node.children.keys()), None
            ):
                if dynamic_part:
                    param_name = dynamic_part.strip("<>").strip()

                    if ":" in param_name:
                        param_type, param_name = param_name.split(":")
                        part = self.convert_param_to_type(part, param_type)

                    params[param_name.strip()] = part
                    node = node.children[dynamic_part]
                else:
                    return None, {}
            else:
                return None, {}

        handler = node.handlers.get(method.upper())
        return handler, params
