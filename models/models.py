from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

import hashlib

from db.database import engine


class Base(DeclarativeBase):
    pass


class User(Base):  # We extend the Base class
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(25))
    last_name = Column(String(25))
    user_name = Column(String(25), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    registration_date = Column(Date(), default=datetime.now)

    def __repr__(self):
        return f"User: [{self.user_name}, {self.first_name} {self.last_name}, {self.registration_date}]"

    def __str__(self):
        return repr(self)

    def set_password(self, password: str):
        self.password = self.hash_password_text(password)

    @classmethod
    def hash_password_text(cls, password):
        return hashlib.sha224(password.encode()).hexdigest()

    def get_user_posts(self):
        return self.posts


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    message = Column(Text)
    created_by_id = Column(Integer, ForeignKey('user.id'))
    created_by = relationship("User", backref='posts')

    def __str__(self):
        return f"Post(id={self.id}, created_by={self.created_by.user_name}, title={self.title}, message={self.message})"

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            message=self.message
        )


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", backref="likes")
    liked_by_id = Column(Integer, ForeignKey('user.id'))
    liked_by = relationship("User", backref='likes')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    post = relationship("Post", backref="comments")
    user = relationship("User", backref="comments")

    def __repr__(self):
        return f'Comment by user {self.user.user_name}: {self.message}'

    def __str__(self):
        return repr(self)

    def to_dict(self):
        return dict(
            id=self.id,
            message=self.message
        )


class Token(Base):
    __tablename__ = 'auth_token'

    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship("User", backref="tokens")


Base.metadata.create_all(bind=engine)
