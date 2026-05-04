from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔐 CLAVE SECRETA (OBLIGATORIO para flash)
app.secret_key = "clave_super_secreta_123"

# =====================
# CONFIG
# =====================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================
# MODELO
# =====================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

# =====================
# CREAR BD
# =====================
with app.app_context():
    db.create_all()

# =====================
# READ
# =====================
@app.route("/")
def index():
    productos = Product.query.all()
    return render_template("index.html", productos=productos)

# =====================
# CREATE
# =====================
@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])

        # Mejora: Validación simple antes de guardar
        if price < 0 or stock < 0:
            flash("Error: El precio y el stock no pueden ser negativos ❌")
            return redirect(url_for("crear"))

        nuevo = Product(name=name, price=price, stock=stock)
        db.session.add(nuevo)
        db.session.commit()

        flash("Producto creado correctamente ✅")
        return redirect(url_for("index"))

    return render_template("crear.html")

# =====================
# UPDATE
# =====================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    # Mejora: Uso de db.session.get() en lugar de Product.query.get()
    producto = db.session.get(Product, id)

    if not producto:
        flash("Producto no encontrado ❌")
        return redirect(url_for("index"))

    if request.method == "POST":
        producto.name = request.form["name"]
        producto.price = float(request.form["price"])
        producto.stock = int(request.form["stock"])

        db.session.commit()

        flash("Producto actualizado correctamente ✅")
        return redirect(url_for("index"))

    return render_template("editar.html", producto=producto)

# =====================
# DELETE
# =====================
@app.route("/eliminar/<int:id>")
def eliminar(id):
    # Mejora: Uso de db.session.get()
    producto = db.session.get(Product, id)

    if not producto:
        flash("Producto no encontrado ❌")
        return redirect(url_for("index"))

    db.session.delete(producto)
    db.session.commit()

    flash("Producto eliminado correctamente 🗑️")
    return redirect(url_for("index"))

# =====================
# RUN
# =====================

if __name__ == "__main__":
    app.run(debug=True)