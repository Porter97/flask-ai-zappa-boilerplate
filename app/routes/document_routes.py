from flask import Blueprint

from app.controllers import DocumentController


document_routes = Blueprint('document_routes', __name__)
document_controller = DocumentController()


