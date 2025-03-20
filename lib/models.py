from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    auditions = relationship('Audition', back_populates='role')

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else 'no actor has been hired for understudy for this role'

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        self.hired = True

# Database setup
engine = create_engine('sqlite:///audition_management.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# CRUD Functions
def create_role(character_name):
    role = Role(character_name=character_name)
    session.add(role)
    session.commit()
    return role

def create_audition(actor, location, phone, role_id):
    audition = Audition(actor=actor, location=location, phone=phone, role_id=role_id)
    session.add(audition)
    session.commit()
    return audition

def get_roles():
    return session.query(Role).all()

def get_auditions():
    return session.query(Audition).all()

def get_role_by_id(role_id):
    return session.query(Role).filter_by(id=role_id).first()

def get_audition_by_id(audition_id):
    return session.query(Audition).filter_by(id=audition_id).first()

def delete_role(role_id):
    role = get_role_by_id(role_id)
    if role:
        session.delete(role)
        session.commit()

def delete_audition(audition_id):
    audition = get_audition_by_id(audition_id)
    if audition:
        session.delete(audition)
        session.commit()
