from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:kimgyusub!001@localhost/TodoApplicationDatabase"

SQLALCHEMY_DATABASE_URI = "postgresql://todoapplicationdatabase_dofj_user:T2hO0jTApIPdIRtwPvlIYl2AUcKMwaA6@dpg-d20q213ipnbc73di87ug-a.singapore-postgres.render.com/todoapplicationdatabase_dofj"
engine = create_engine(SQLALCHEMY_DATABASE_URI,
    connect_args={"sslmode": "require"} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


