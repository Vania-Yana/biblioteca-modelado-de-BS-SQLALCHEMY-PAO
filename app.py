from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vania2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        product = Product(
            name=request.form["name"],
            price=float(request.form["price"]),
            stock=int(request.form["stock"])
        )
        db.session.add(product)
        db.session.commit()
        flash("Producto creado correctamente", "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        db.session.commit()
        flash("Producto actualizado correctamente", "primary")
        return redirect(url_for("index"))
    return render_template("edit.html", product=product)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Producto eliminado correctamente", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)