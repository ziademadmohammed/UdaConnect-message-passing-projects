from app.location.models import Location # noqa
from app.location.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.location.controllers import api as location_api

    api.add_namespace(location_api, path=f"/{root}")
