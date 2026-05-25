import os
from flask import Flask, send_from_directory
from app.database import db


def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///jogaai.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "joga-ai-secret-dev-key-2024")

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.jogos import jogos_bp
    from app.routes.emprestimos import emprestimos_bp
    from app.routes.chat import chat_bp
    from app.routes.penalidades import penalidades_bp
    from app.routes.notificacoes import notificacoes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jogos_bp)
    app.register_blueprint(emprestimos_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(penalidades_bp)
    app.register_blueprint(notificacoes_bp)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.template_folder, "index.html")

    with app.app_context():
        db.create_all()

    return app