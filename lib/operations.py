from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Role, Audition, Base

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

# Insert sample data
role1 = create_role("Hamlet")
role2 = create_role("Ophelia")

audition1 = create_audition("John Doe", "New York", 1234567890, role1.id)
audition2 = create_audition("Jane Smith", "Los Angeles", 9876543210, role2.id)

# Display inserted data
print("Roles:", [role.character_name for role in get_roles()])
print("Auditions:", [(aud.actor, aud.location) for aud in get_auditions()])
