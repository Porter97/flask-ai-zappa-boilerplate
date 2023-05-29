from flask import make_response
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app.middlewares.auth_middleware import get_current_user
from app.middlewares.logger_middleware import log_request_info, log_response_info
from app.routes.document_routes import document_routes
from app.routes.user_routes import user_routes

from app.utils.messages import Error
from app.utils.response import Response


def stop(env, resp):
    resp('200 OK', [('Content-Type', 'text/plain')])
    return [b'Boilerplate API. Basepath /v1/']


blueprints = {
    '/documents': document_routes,
    '/users': user_routes,
}


def init_routes(app):
    app.wsgi_app = DispatcherMiddleware(stop, {'/v1': app.wsgi_app})

    app.before_request(get_current_user)
    app.before_request(log_request_info)
    app.after_request(log_response_info)

    for path in blueprints:
        app.register_blueprint(blueprints[path], url_prefix=path)

    @app.get("/")
    def index():
        return Response({'api_version': 'v1.0', 'api_description': 'Boilerplate API'},
                        Response.HTTP_SUCCESS).build()

    @app.get("/health")
    def health():
        return Response({'status': 'online'}, Response.HTTP_SUCCESS).build()

    @app.errorhandler(404)
    def not_found_error(error):
        return make_response(Error.NOT_FOUND, Response.HTTP_NOT_FOUND)

    @app.errorhandler(401)
    def unauthorized_error(error):
        return make_response(Error.UNAUTHORIZED, Response.HTTP_UNAUTHORIZED)

    @app.errorhandler(400)
    def bad_request_error(error):
        return make_response(Error.BAD_REQUEST, Response.HTTP_BAD_REQUEST)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(Error.INTERNAL_SERVER_ERROR, Response.HTTP_ERROR)
