from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tabla intermedia student_course
student_course = db.Table(
    "student_course",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True)
)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    courses = db.relationship("Course", secondary=student_course, back_populates="students")

    def __repr__(self):
        return f"<Estudiante: nombre={self.name}>"

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    students = db.relationship("Student", secondary=student_course, back_populates="courses")

    def __repr__(self):
        return f"<Curso: titulo={self.title}>"

# Inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Base de datos creada satisfactoriamente")

# Insertar registros
def insert_data():
    with app.app_context():
        # Verifica si ya hay datos para no duplicar
        if Student.query.first():
            print("⚠️ Ya existen datos. No se insertan duplicados.")
            return
            
        # Crear estudiantes
        s1 = Student(name="Bruno Diaz")
        s2 = Student(name="Zacarias Flores")
        s3 = Student(name="Elsa Capunta")
        
        # Crear cursos
        c1 = Course(title="Python")
        c2 = Course(title="Javascript")
        c3 = Course(title="React")
        
        s1.courses.extend([c1, c2])  # Registro de Bruno a Python y Javascript
        s2.courses.append(c2)        # Registro de Zacarias a Javascript
        s3.courses.extend([c1, c3])  # Registro de Elsa a Python y React
        
        db.session.add_all([s1, s2, s3, c1, c2, c3])
        db.session.commit()
        print("✅ Estudiantes y cursos insertados correctamente")

def update_relations():
    with app.app_context():
        print("\n🔄 Agregando un curso a un estudiante")
        estu = Student.query.filter_by(id=1).first()
        curso = Course.query.filter_by(id=3).first()  # Le agrego React a Bruno
        if estu and curso and curso not in estu.courses:
            estu.courses.append(curso)
            db.session.commit()
            print("✅ Inscripción actualizada")
        else:
            print("⚠️ El estudiante o curso no existe, o ya está inscrito")

def delete_relation():
    with app.app_context():
        print("\n🗑️ Eliminación de la inscripción en un curso")
        estu = Student.query.filter_by(id=1).first()
        curso = Course.query.filter_by(id=2).first()  # Le quito Javascript a Bruno
        if estu and curso and curso in estu.courses:
            estu.courses.remove(curso)
            db.session.commit()
            print("✅ Se eliminó la inscripción")
        else:
            print("⚠️ No existe esa inscripción")

def query_data():
    with app.app_context():
        print("\n📋 Listado de estudiantes y cursos")
        students = Student.query.all()
        for s in students:
            print(f"\n{s.name} está inscrito en:")
            if s.courses:
                for c in s.courses:
                    print(f" - {c.title}")
            else:
                print(" - No tiene cursos inscritos")
                
        print("\n📋 Listado de cursos y sus estudiantes")
        courses = Course.query.all()
        for c in courses:
            print(f"\n{c.title} tiene inscritos a:")
            if c.students:
                for s in c.students:
                    print(f" - {s.name}")
            else:
                print(" - No tiene estudiantes inscritos")

if __name__ == "__main__":
    init_db()        # 1. Crea las tablas - solo corre 1 vez
    insert_data()    # 2. Mete datos - no duplica si ya existen
    query_data()     # 3. Muestra todo
    
    # Descomenta estas si quieres probar:
    # update_relations()
    # delete_relation()
    # query_data()     # Para ver los cambios