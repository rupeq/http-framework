from http_framework.routing import RoutingMixin


class Blueprint(RoutingMixin):
    """
    Blueprint class. This class is used to create blueprints.
    """

    def __init__(self, name: str, prefix: str = "") -> None:
        super().__init__()
        self.name = name
        self.prefix = prefix

        if not self.prefix.endswith("/"):
            self.prefix += "/"
