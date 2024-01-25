from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, \
    select
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# postgresql://логин:пароль@имя хоста:порт/имя БД
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres',
                       echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def main():
    session = Session()
    stmt = select(Book).where(Book.title == 'Робинзон Крузо')
    for book in session.scalars(stmt):
        print(book, '\n', book.reviews, '\n', book.reviews[0].text)


def fill():
    Base.metadata.create_all(engine)
    session = Session()

    # Создаём книги
    session.add(Book(title='Робинзон Крузо', author='Даниэль Дэфо'))
    session.add(Book(title='Путешествие к центру земли', author='Жуль Верн'))

    # Создаём пользователей
    session.add(User(name='user1'))
    session.add(User(name='user2'))

    # Создаём отзывы
    session.add(Reviews(text='Замечательный роман о приключениях Робинзона',
                        book_id=1, user_id=1))
    session.add(Reviews(text='Замечательный роман о'
                             ' путешествии к центру земли',
                        book_id=2, user_id=2))
    session.add(Reviews(text='Мне не понравилось', book_id=1, user_id=2))
    session.commit()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    author = Column(String(30), nullable=False)
    reviews = relationship('Reviews', backref='book', lazy=True)
    def __repr__(self):
        return self.title


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String(2000), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'От {self.reviewer}'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    reviews = relationship('Reviews', backref='reviewer', lazy=True)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    main()
