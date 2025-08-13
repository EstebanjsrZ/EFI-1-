from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Usuario, Post, Comentario, Categoria

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    cat = request.args.get("cat")
    query = Post.query.order_by(Post.creado_en.desc())
    if q:
        like = f"%{q}%"
        query = query.filter((Post.titulo.ilike(like)) | (Post.contenido.ilike(like)))
    if cat:
        query = query.join(Post.categorias).filter(Categoria.id == cat)
    posts = query.all()
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    return render_template("index.html", posts=posts, categorias=categorias, q=q, cat=cat)

@bp.route("/usuarios/nuevo", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        nombre = request.form.get("nombre_usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "").strip()
        if not (nombre and correo and password):
            flash("Completá todos los campos.", "error")
            return redirect(url_for("main.new_user"))
        if Usuario.query.filter((Usuario.nombre_usuario == nombre) | (Usuario.correo == correo)).first():
            flash("Nombre de usuario o correo ya existe.", "error")
            return redirect(url_for("main.new_user"))
        user = Usuario(nombre_usuario=nombre, correo=correo, password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado.", "success")
        return redirect(url_for("main.index"))
    return render_template("new_user.html")

@bp.route("/categorias/nueva", methods=["GET", "POST"])
def new_category():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("Ingresá un nombre.", "error")
            return redirect(url_for("main.new_category"))
        if Categoria.query.filter_by(nombre=nombre).first():
            flash("Ya existe esa categoría.", "error")
            return redirect(url_for("main.new_category"))
        db.session.add(Categoria(nombre=nombre))
        db.session.commit()
        flash("Categoría creada.", "success")
        return redirect(url_for("main.index"))
    return render_template("new_category.html")

@bp.route("/posts/nuevo", methods=["GET", "POST"])
def new_post():
    usuarios = Usuario.query.order_by(Usuario.nombre_usuario.asc()).all()
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()
        autor_id = request.form.get("autor_id")
        cat_ids = request.form.getlist("categorias")
        if not (titulo and contenido and autor_id):
            flash("Completá título, contenido y autor.", "error")
            return redirect(url_for("main.new_post"))
        post = Post(titulo=titulo, contenido=contenido, autor_id=int(autor_id))
        if cat_ids:
            post.categorias = Categoria.query.filter(Categoria.id.in_(cat_ids)).all()
        db.session.add(post)
        db.session.commit()
        flash("Post creado.", "success")
        return redirect(url_for("main.post_detail", post_id=post.id))
    return render_template("new_post.html", usuarios=usuarios, categorias=categorias)

@bp.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@bp.route("/posts/<int:post_id>/editar", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    usuarios = Usuario.query.order_by(Usuario.nombre_usuario.asc()).all()
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    if request.method == "POST":
        post.titulo = request.form.get("titulo", "").strip()
        post.contenido = request.form.get("contenido", "").strip()
        post.autor_id = int(request.form.get("autor_id"))
        cat_ids = request.form.getlist("categorias")
        post.categorias = Categoria.query.filter(Categoria.id.in_(cat_ids)).all() if cat_ids else []
        db.session.commit()
        flash("Post actualizado.", "success")
        return redirect(url_for("main.post_detail", post_id=post.id))
    return render_template("edit_post.html", post=post, usuarios=usuarios, categorias=categorias)

@bp.route("/posts/<int:post_id>/eliminar", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post eliminado.", "success")
    return redirect(url_for("main.index"))

@bp.route("/posts/<int:post_id>/comentarios/nuevo", methods=["GET", "POST"])
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    usuarios = Usuario.query.order_by(Usuario.nombre_usuario.asc()).all()
    if request.method == "POST":
        texto = request.form.get("texto", "").strip()
        autor_id = request.form.get("autor_id")
        if not (texto and autor_id):
            flash("Completá el texto y el autor.", "error")
            return redirect(url_for("main.new_comment", post_id=post.id))
        com = Comentario(texto=texto, autor_id=int(autor_id), post_id=post.id)
        db.session.add(com)
        db.session.commit()
        flash("Comentario agregado.", "success")
        return redirect(url_for("main.post_detail", post_id=post.id))
    return render_template("new_comment.html", post=post, usuarios=usuarios)

@bp.route("/comentarios/<int:comentario_id>/eliminar", methods=["POST"])
def delete_comment(comentario_id):
    comentario = Comentario.query.get_or_404(comentario_id)
    post_id = comentario.post_id
    db.session.delete(comentario)
    db.session.commit()
    flash("Comentario eliminado.", "success")
    return redirect(url_for("main.post_detail", post_id=post_id))
