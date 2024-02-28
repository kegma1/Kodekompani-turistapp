from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, LargeBinary, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
#from libs.pfp import make_profile

# Import database configuration variables
# from db_connection_config import HOST, USER, PASSWORD, DATABASE
from db_connection_config import HOST, USER, PASSWORD, DATABASE

# Database URL and Engine Setup
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URL, echo=True)

# Session and Base Setup
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)
Base = declarative_base()

# Model Definitions
class Friend(Base):
    __tablename__ = 'friends'
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    friend_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    
class User(Base):
    __tablename__ = 'users_turistapp'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(DATE)
    full_name = Column(String(63))
    bio = Column(String(255))
    encrypted_password = Column(String(255), nullable=False)
    isAdmin = Column(Boolean)
    profile_pic = Column(LargeBinary)
    attractions = relationship("Attraction", secondary="user_attractions")
    achievements = relationship("Achievement", secondary="user_achievements")
    friends = relationship("User", 
                           secondary="friends",
                           primaryjoin=id==Friend.user_id,
                           secondaryjoin=id==Friend.friend_id)

    def __init__(self, username, email, password, full_name, data_of_birth):
        self.username = username
        self.email = email
        self.age = data_of_birth
        self.encrypted_password = password
        self.isAdmin = False
        self.profile_pic = make_profile(username, 400, 50).read()
        self.full_name = full_name
        self.bio = ""


class Attraction(Base):
    __tablename__ = 'attractions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    category = Column(String(50))
    age_recommendation = Column(String(20))
    location_coordinates = Column(String(100))

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    criteria = Column(String(255))

class UserAttraction(Base):
    __tablename__ = 'user_attractions'
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)

# Create All Tables in the Database
def create_tables():
    Base.metadata.create_all(engine)
    
# Delete All Tables in the Database
def delete_tables():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    create_tables()
    #delete_tables()
