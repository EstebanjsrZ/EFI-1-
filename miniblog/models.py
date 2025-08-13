from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

post_categorias = db.Table(
    "post_categorias",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("categoria_id", db.Integer, db.ForeignKey("categorias.id"), primary_key=True),
)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    posts = db.relationship("Post", back_populates="autor", cascade="all, delete")
    comentarios = db.relationship("Comentario", back_populates="autor", cascade="all, delete")

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    creado_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    autor = db.relationship("Usuario", back_populates="posts")

    comentarios = db.relationship("Comentario", back_populates="post", cascade="all, delete-orphan")

    categorias = db.relationship(
        "Categoria",
        secondary=post_categorias,
        back_populates="posts",
    )

    def __repr__(self):
        return f"<Post {self.titulo[:15]}>"

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    creado_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    autor = db.relationship("Usuario", back_populates="comentarios")

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", back_populates="comentarios")

    def __repr__(self):
        return f"<Comentario {self.id} por {self.autor_id}>"

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    posts = db.relationship(
        "Post",
        secondary=post_categorias,
        back_populates="categorias",
    )

    def __repr__(self):
        return f"<Categoria {self.nombre}>"
