from flask import render_template, jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        if request_wants_json():
            return jsonify(error=str(error)), 400
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        if request_wants_json():
            return jsonify(error='Unauthorized'), 401
        return render_template('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        if request_wants_json():
            return jsonify(error='Forbidden'), 403
        return render_template('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def not_found(error):
        if request_wants_json():
            return jsonify(error='Not found'), 404
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        if request_wants_json():
            return jsonify(error='Internal server error'), 500
        return render_template('errors/500.html', error=error), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        
        app.logger.error(f'Unhandled exception: {str(error)}')
        if request_wants_json():
            return jsonify(error='Internal server error'), 500
        return render_template('errors/500.html', error=error), 500

def request_wants_json():
    """Check if the request wants JSON response."""
    from flask import request
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > request.accept_mimetypes['text/html'] 