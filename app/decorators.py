import functools
import traceback
from collections import defaultdict
from functools import wraps

from flask import abort, g, request
from marshmallow import ValidationError

from app import logger
from app.errors import ProcessingException, ValidationException
from app.models.user_model import Permission
from app.utils.messages import Error
from app.utils.response import Response


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'current_user'):
                abort(403)
            if not g.current_user.get('permissions') >= permission:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationException as ve:
            logger.info(str(ve.messages))
            return Response.make(ve.messages, Response.HTTP_BAD_REQUEST)
        except ProcessingException as pe:
            logger.info(str(pe.messages))
            return Response.make(pe.messages, Response.HTTP_BAD_REQUEST)
        except ValidationError as err:
            logger.info(err)
            return Response.make(err.messages, Response.HTTP_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            logger.error(f'general exception {e}')
            return Response.make(Error.REQUEST_FAILED, Response.HTTP_ERROR)
    return wrapper
