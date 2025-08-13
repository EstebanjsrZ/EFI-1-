from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import bp as main_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_categories():
        from models import Categoria
        try:
            categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
        except Exception:
            categorias = []
        return {"all_categories": categorias}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
