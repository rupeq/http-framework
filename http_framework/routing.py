from typing import Callable, Any

HandlerType = Callable[..., Any]


class RoutingMixin:
    """
    A mixin for adding routing functionality to a class.
    """

    def __init__(self) -> None:
        self.route_configurations = []
        self.routes = ...

    @staticmethod
    def _split_path(path: str) -> list[str]:
        """
        Splits a URL path into a list of path segments.

        Parameters:
            - path: The URL path to split.

        Returns:
            A list of path segments.
        """

        return path.strip("/").split("/")

    def route(self, path: str, methods: list[str] | None = None) -> Callable:
        """
        A decorator that registers a view function for a given path and HTTP method.

        Parameters:
            - path: The URL path to register the view function for.
            - methods: A list of HTTP methods to register the view function for. If not provided, the view function will
            be registered for all HTTP methods.

        Returns:
            A decorator that registers a view function for a given path and HTTP method.
        """
        if not methods:
            methods = ["GET"]

        path = self._split_path(path)

        def decorator(view_func: HandlerType) -> HandlerType:
            """
            A decorator function that appends route configurations and inserts them into the routes if applicable.

            Parameters:
                view_func: the view function to be decorated.

            Returns:
                The decorated view function.
            """

            self.route_configurations.append((path, methods, view_func))
            if (
                self.routes
                and hasattr(self.routes, "insert")
                and callable(self.routes.insert)
            ):
                self.routes.insert(path, methods, view_func)

            return view_func

        return decorator
