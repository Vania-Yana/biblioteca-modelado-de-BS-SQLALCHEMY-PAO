# RELACIONES 1 - N con ORM

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Declaracion para usar Alchemy como ORM
db = SQLAlchemy(app)

#Definicion del modelo de datos
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #parametro para eliminar elementos relacinados se usa "cascade='all, delete-orphan'"
    #relacion con la clase Post
    posts = db.relationship('Post', back_populates='user',cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #llave foranea que establece la relacion con la tabla users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    #relacion con la clase User
    user = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f"Post:title:{self.title} user: {self.user.name} email: {self.user.email} content: {self.content}"

#funcion para inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada")
        
#CRUD
def insert_data():
    with app.app_context():
        #intanciacion de objetos de la clase User y Post
        user1= User(name="Carlos Meruvia", email="carlos.meruvia@gmail.com")
        user2= User(name="Richard Tapia", email="rick@gmail.com")
        user3= User(name="Antonio Zepita", email="antonio.zepita@gmail.com")
        
        post1 = Post(title="Primer Post", content="Primera publicacion de Carlos", user=user1)
        post2 = Post(title="Segundo Post", content="Primera publicacion de Richard", user=user2)
        post3 = Post(title="Tercer Post", content="Segunda publicacion de Carlos", user=user1)
        post4 = Post(title="Cuarto Post", content="Primera publicacion de Antonio", user=user3)
        
        db.session.add_all((user1, user2, user3, post1, post2, post3, post4))
        
        db.session.commit()
        print(f"Datos insertados")


def query_data():
    with app.app_context():
        print("Listado de Usuarios y sus publicaciones:")
        users = User.query.all()
        for user in users:
            print(user)
            for post in user.posts:
                print(post)

def update_data():
    with app.app_context():
        print("Actualizando una publicacion")
        post = Post.query.filter_by(id=3).first().user
        if post:
            post.content = "Entrada ACTUALIZADA de Richard"
            db.session.commit()
            print(f"Publicacion actualizada para")
        else:
            print("Publicacion no encontrada")  

def delete_data():
    with app.app_context():
        print("Eliminando una usuarios en cascada")
        user = User.query.filter_by(id=1).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"Usuario {user.name} eliminado junto con sus publicaciones")
        else:
            print("Publicacion no encontrada")    
            

if __name__ == '__main__':
    init_db()
    insert_data()   
    query_data()
    update_data()
    delete_data()