# Приложение Flask с SQLAlchemy
import random

from flask import Flask, render_template
from database import db, Book, Genre

app = Flask(__name__)
# лучше делать через переменную окружения
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db.init_app(app)


# Создадим базу данных прямо здесь
with app.app_context():
    db.drop_all()
    db.create_all()
    # Добавим тестовые данные
    fiction = Genre(name="Фантастика")
    comedy = Genre(name="Комедия")
    detective = Genre(name="Детектив")
    db.session.add(fiction)
    db.session.add(comedy)
    db.session.add(detective)

    for x in range(100):
        g = random.randint(1,3)
        if g == 1: db.session.add(Book(name=f"книга {x}", genre=fiction))
        if g == 2: db.session.add(Book(name=f"книга {x}", genre=comedy))
        if g == 3: db.session.add(Book(name=f"книга {x}", genre=detective))

    db.session.commit()



@app.route("/")
def all_books():
    # Здесь порядок будет по id, так как при инициализации БД в тестовом режиме,
    # все книги создаются почти одновременно и сортировка по времени создания не работает

    # books = Book.query.order_by(Book.added.desc()).limit(15)
    books = Book.query.order_by(Book.id.desc()).limit(15)
    return render_template("all_books.html", books=books)


@app.route("/genre/<int:genre_id>")
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genre.html",
        genre_name=genre.name,
        books=genre.books
    )


if __name__ == "__main__":
    app.run()
