from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)

all_books = []

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    ##READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_books = result.scalars()
    return render_template("index.html", books=all_books)

#define uma rota para a página de adição de livros
@app.route("/add", methods=["GET", "POST"])
def add():
    #se o formulário for submetido, ele cria um novo dicionário
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)  # Adiciona o objeto Book ao banco de dados
        db.session.commit()

        return redirect(url_for('home'))
         
    return render_template("add.html")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    # Encontre o livro no banco de dados pelo ID
    book = Book.query.get(id)
    if book:
        # Remova o livro do banco de dados
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        # Lidar com o caso em que o livro não foi encontrado
        return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    the_book = Book.query.get(id)
 
    if request.method == 'POST':
        the_book.rating = request.form['new-rating']
        db.session.commit()
        return redirect(url_for('home'))
 
    return render_template("edit_rating.html", book=the_book)

if __name__ == "__main__":
    app.run(debug=True)
