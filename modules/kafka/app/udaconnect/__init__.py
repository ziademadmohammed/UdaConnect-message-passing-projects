def register_routes(api, app, root="location_api"):
    from controllers import api as udaconnect_location_api

    api.add_namespace(udaconnect_location_api, path=f"/{root}")
