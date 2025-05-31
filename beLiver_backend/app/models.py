from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    projects = relationship('Project', back_populates='user', cascade='all, delete-orphan')
    chat_histories = relationship('ChatHistory', back_populates='user', cascade='all, delete-orphan')


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    summary = Column(Text)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    estimated_loading = Column(Numeric(3, 1))
    due_date = Column(Date)
    current_milestone = Column(String(255))  # 純文字，不建立 FK 關聯
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='projects')
    milestones = relationship('Milestone', back_populates='project', cascade='all, delete-orphan')
    files = relationship('File', back_populates='project', cascade='all, delete-orphan')
    chat_histories = relationship('ChatHistory', back_populates='project', cascade='all, delete-orphan')


class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    summary = Column(Text)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    estimated_loading = Column(Numeric(3, 1))
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))

    project = relationship('Project', back_populates='milestones')
    tasks = relationship('Task', back_populates='milestone', cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(Date)
    estimated_loading = Column(Numeric(3, 1))
    milestone_id = Column(Integer, ForeignKey('milestones.id', ondelete='SET NULL'))
    is_completed = Column(Boolean, default=False)

    milestone = relationship('Milestone', back_populates='tasks')


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))

    project = relationship('Project', back_populates='files')


class ChatHistory(Base):
    __tablename__ = 'chat_histories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    message = Column(Text, nullable=False)
    sender = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship('User', back_populates='chat_histories')
    project = relationship('Project', back_populates='chat_histories')
