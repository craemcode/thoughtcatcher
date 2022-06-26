#Database Models
# USER, TOPICS, THOUGHTS


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




db = SQLAlchemy()

class Todo():
    pass

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(69))
    

    topics = db.relationship('Topic', backref='user')
    

    def __repr__(self):
        return f'User {self.name}'

#Many topics belong to a single user. a query can determine the topics for
#a user and vice versa.
class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(69))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    thoughts = db.relationship('Thought', backref='topic')
    
    def __repr__(self):
        return f'Topic {self.name}'

#a topic can have many thoughts associated with it. However, each thought can belong to one 
#topic
class Thought(db.Model):
    __tablename__ = 'thoughts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __repr__(self):
        return f'Thought: {self.content}'