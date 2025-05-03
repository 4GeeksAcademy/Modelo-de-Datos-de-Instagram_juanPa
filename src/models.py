from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()
       


follower_association = db.Table(
    'follower',
    db.Column('user_from_id', Integer, db.ForeignKey(
        'users.id'), primary_key=True),
    db.Column('user_to_id', Integer, db.ForeignKey(
        'users.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    following:Mapped[List["User"]]=relationship(
        'User',
        secondary= follower_association,
        primaryjoin=(id==follower_association.c.user_from_id),
        secondaryjoin=(id==follower_association.c.user_to_id),
        back_populates="followers"
    )

    followers:Mapped[List["User"]]=relationship(
        'User',
        secondary= follower_association,
        primaryjoin=(id==follower_association.c.user_to_id),  
        secondaryjoin=(id==follower_association.c.user_from_id),
        back_populates="following"
    )




class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable=False)


    author: Mapped["User"] = relationship(back_populates="comment")
    post: Mapped["Post"] = relationship(back_populates="comment")



class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)


    user: Mapped["User"] = relationship(back_populates="post")
    media: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")



class Media(db.Model):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable=False)


    post: Mapped["Post"] = relationship(back_populates="media")
















































    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
