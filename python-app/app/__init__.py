from flask import Flask, redirect, url_for
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        # Import models
        from app.models import Theater, Screen, Booking, User, FoodBeverage
        
        # Import and register blueprints
        from app.routes.theater_routes import bp as theater_bp
        from app.routes.booking_routes import bp as booking_bp
        
        app.register_blueprint(theater_bp, url_prefix='/theater')
        app.register_blueprint(booking_bp, url_prefix='/booking')
        
        # Redirect root to theater index
        @app.route('/')
        def index():
            return redirect(url_for('theater.index'))
        
        # Create database tables
        db.create_all()
        
        # Initialize database with sample data
        from app.utils.db_init import init_db
        init_db()
    
    return app