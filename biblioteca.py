from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tabla intermedia N-M para Libro-Genero
libro_genero = db.Table(
    "libro_genero",
    db.Column("libro_id", db.Integer, db.ForeignKey("libros.id"), primary_key=True),
    db.Column("genero_id", db.Integer, db.ForeignKey("generos.id"), primary_key=True)
)

class Autor(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    
    # Relacion 1-N: Un autor tiene muchos libros
    # cascade='all, delete-orphan' = si borro autor, borro sus libros
    libros = db.relationship('Libro', back_populates='autor', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Autor: {self.nombre}, {self.nacionalidad}>"

class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    
    # Llave foranea 1-N: Un libro tiene un solo autor
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    autor = db.relationship('Autor', back_populates='libros')
    
    # Relacion N-M: Un libro tiene varios generos
    generos = db.relationship('Genero', secondary=libro_genero, back_populates='libros')

    def __repr__(self):
        return f"<Libro: {self.titulo}, {self.anio}>"

class Genero(db.Model):
    __tablename__ = 'generos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relacion N-M: Un genero tiene varios libros
    libros = db.relationship('Libro', secondary=libro_genero, back_populates='generos')

    def __repr__(self):
        return f"<Genero: {self.nombre}>"

# REQUERIMIENTO 1: init_db() — crear la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

# REQUERIMIENTO 2: insertar_datos() — mínimo 3 autores, 5 libros, 4 generos
def insertar_datos():
    with app.app_context():
        if Autor.query.first():
            print("Ya existen datos. No se insertan duplicados.")
            return
            
        # 3 Autores
        a1 = Autor(nombre="Gabriel García Márquez", nacionalidad="Colombiana")
        a2 = Autor(nombre="Isabel Allende", nacionalidad="Chilena")
        a3 = Autor(nombre="Jorge Luis Borges", nacionalidad="Argentina")
        
        # 4 Generos
        g1 = Genero(nombre="Ficción")
        g2 = Genero(nombre="Realismo Mágico")
        g3 = Genero(nombre="Cuento")
        g4 = Genero(nombre="Novela")
        
        # 5 Libros con sus asociaciones
        l1 = Libro(titulo="Cien años de soledad", anio=1967, autor=a1)
        l1.generos.extend([g1, g2, g4])
        
        l2 = Libro(titulo="El amor en los tiempos del cólera", anio=1985, autor=a1)
        l2.generos.extend([g1, g4])
        
        l3 = Libro(titulo="La casa de los espíritus", anio=1982, autor=a2)
        l3.generos.extend([g1, g2, g4])
        
        l4 = Libro(titulo="Ficciones", anio=1944, autor=a3)
        l4.generos.extend([g1, g3])
        
        l5 = Libro(titulo="El Aleph", anio=1949, autor=a3)
        l5.generos.extend([g1, g3])
        
        db.session.add_all([a1, a2, a3, g1, g2, g3, g4, l1, l2, l3, l4, l5])
        db.session.commit()
        print("Autores, libros y géneros insertados correctamente")

# REQUERIMIENTO 3: consultar_datos() — listar autores con libros, y generos con libros
def consultar_datos():
    with app.app_context():
        print("\nLISTADO DE AUTORES Y SUS LIBROS")
        autores = Autor.query.all()
        for autor in autores:
            print(f"\nAutor: {autor.nombre} - {autor.nacionalidad}")
            if autor.libros:
                for libro in autor.libros:
                    generos_libro = ", ".join([g.nombre for g in libro.generos])
                    print(f"   Libro: {libro.titulo} ({libro.anio}) | Géneros: {generos_libro}")
            else:
                print("   No tiene libros registrados")
        
        print("\nLISTADO DE GÉNEROS Y SUS LIBROS")
        generos = Genero.query.all()
        for genero in generos:
            print(f"\nGénero: {genero.nombre}")
            if genero.libros:
                for libro in genero.libros:
                    print(f"   Libro: {libro.titulo} - Autor: {libro.autor.nombre}")
            else:
                print("   No tiene libros registrados")

# REQUERIMIENTO 4: actualizar_datos() — actualizar el titulo de un libro
def actualizar_datos():
    with app.app_context():
        print("\nACTUALIZANDO TÍTULO DE UN LIBRO")
        libro = Libro.query.filter_by(titulo="El Aleph").first()
        if libro:
            titulo_anterior = libro.titulo
            libro.titulo = "El Aleph - Edición Actualizada"
            db.session.commit()
            print(f"Libro actualizado: '{titulo_anterior}' -> '{libro.titulo}'")
        else:
            print("Libro no encontrado")

# REQUERIMIENTO 5: eliminar_datos() — eliminar un autor (sus libros deben eliminarse en cascada)
def eliminar_datos():
    with app.app_context():
        print("\nELIMINANDO UN AUTOR EN CASCADA")
        autor = Autor.query.filter_by(nombre="Isabel Allende").first()
        if autor:
            nombre_autor = autor.nombre
            libros_count = len(autor.libros)
            db.session.delete(autor)
            db.session.commit()
            print(f"Autor '{nombre_autor}' eliminado junto con {libros_count} libros")
        else:
            print("Autor no encontrado")

if __name__ == "__main__":
    init_db()
    insertar_datos()
    consultar_datos()
    actualizar_datos()
    eliminar_datos()
    print("\n" + "="*50)
    consultar_datos()