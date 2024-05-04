from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, LargeBinary, DATE, text, func, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from libs.pfp import make_profile
from base64 import b64encode
from io import BytesIO
from PIL import Image

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
    isDeleted = Column(Boolean, default= False)
    xp_collected = Column(Integer, default=0)
    _profile_pic = Column("profile_pic" , LargeBinary)
    attractions = relationship("Attraction", secondary="user_attractions")
    achievements = relationship("Achievement", secondary="user_achievements")
    posts = relationship('UserPosts', back_populates='user')
    
    attractions = relationship("Attraction", back_populates="local_admin")

    following = relationship("User", 
                             secondary="friends",
                             primaryjoin=id==Friend.user_id,
                             secondaryjoin=id==Friend.friend_id)
                             
    followers = relationship("User", 
                             secondary="friends",
                             primaryjoin=id==Friend.friend_id,
                             secondaryjoin=id==Friend.user_id)
    
    

    def __init__(self, username, email, password, full_name, data_of_birth):
        self.username = username
        self.email = email
        self.age = data_of_birth
        self.encrypted_password = password
        self.isAdmin = False
        self._profile_pic = make_profile(username, 200, 25).read()
        self.full_name = full_name
        self.bio = ""
        
    @property
    def profile_pic(self):
        return b64encode(self._profile_pic).decode('utf-8')
    
    @profile_pic.setter
    def profile_pic(self, new_pic):
        if new_pic:
            buffer = BytesIO()
            image = Image.open(new_pic)
            image = image.resize((200, 200))
            
            image.save(buffer, format="PNG", quality=20, optimize=True)

            buffer.seek(0)
            self._profile_pic = buffer.read()
        else:
            default_picture = make_profile(self.username, 200, 25)
            self._profile_pic = default_picture.read()

class Attraction(Base):
    __tablename__ = 'attractions'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    category = Column(String(50))
    age_recommendation = Column(Integer)
    location_coordinates = Column(String(100))
    address = Column(String(100))
    _image = Column("image", LargeBinary(length=(2**32)-1), nullable=True)
    group = Column(Integer, default=None)
    keywords = Column(String(100))
    isDeleted = Column(Boolean, default=False)
    achievements = relationship('Achievement', back_populates='attraction')
    posts = relationship('UserPosts', back_populates='attraction')
    
    local_admin_id = Column(Integer, ForeignKey('users_turistapp.id'))
    local_admin = relationship("User", back_populates="attractions")

    @property
    def image(self):
        if self._image is not None:
            return b64encode(self._image).decode('utf-8')
        else:
            return None
    
    @image.setter
    def image(self, new_pic):

        buffer = BytesIO()
        image = Image.open(new_pic)
        image = image.resize((500, 500))
        
        image.save(buffer, format="PNG", quality=20, optimize=True)

        buffer.seek(0)
        self._image = buffer.read()

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    pass_code = Column(String(255))
    xp_reward = Column(Integer)
    attraction_id = Column(Integer, ForeignKey('attractions.id'))
    attraction = relationship('Attraction', back_populates='achievements')
    age_rating = Column(Integer, default= 0)
    is_deleted = Column(Boolean, default=0)

class UserAttraction(Base):
    __tablename__ = 'user_attractions'
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)

class UserPosts(Base):
    __tablename__ = 'user_posts'
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_turistapp.id'), nullable=False)
    user = relationship('User', back_populates="posts")
    post = Column(String(255), nullable=False)
    _image = Column("image", LargeBinary(length=(2**32)-1), nullable=True)
    time = Column(TIMESTAMP, default=func.now(), nullable=False)
    attraction_id = Column(Integer, ForeignKey('attractions.id'), nullable=True)
    attraction = relationship('Attraction', back_populates=None)
    isDeleted = Column(Boolean, default= False)
    is_status = Column(Boolean, default= False)

    def __init__(self, message, user, attraction = 0, is_status = False):
        self.user_id = user
        self.post = message

        self.is_status = is_status

        if int(attraction) > 0:
            self.attraction_id = attraction
        else:
            self.attraction_id = None

    @property
    def image(self):
        if self._image is not None:
            return b64encode(self._image).decode('utf-8')
        else:
            return None
    
    @image.setter
    def image(self, new_pic):
        if new_pic:
            buffer = BytesIO()
            image = Image.open(new_pic)
            image = image.resize((500, 500))
            
            image.save(buffer, format="PNG", quality=20, optimize=True)

            buffer.seek(0)
            self._image = buffer.read()
        else:
            self._image = None

# Create All Tables in the Database
def create_tables():
    Base.metadata.create_all(engine)
    
# Delete All Tables in the Database
def delete_tables():
    Base.metadata.drop_all(engine)

def insert_test_data():
    with engine.connect() as con:
        with open("./testdata.sql", "r", encoding="utf-8") as file:
            queries = file.read().split(';')

            for query in queries:
                if query.strip():  # Skip empty queries
                    con.execute(text(query))
        con.commit()


if __name__ == "__main__":
    delete_tables()
    create_tables()
    insert_test_data()

