from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///config_file.db', echo=True)
Base = declarative_base()


########################################################################
class GRConfig(Base): # generic class in laying out template for DB implementation
    """"""
    __tablename__ = "Configuration"

    ID = Column(Integer, primary_key=True) # Set Type for each input, this will be taken as
    name = Column(String)
    value_one = Column(String)
    value_two = Column(Float)
    value_three = Column(Float)
    value_four = Column(Float)
    value_five = Column(Float)
    value_six = Column(Float)
    value_seven = Column(Float)

    # ----------------------------------------------------------------------
    def __init__(self, ID , name, value_one, value_two, value_three, value_four, value_five, value_six, value_seven):

        self.ID = ID
        self.name = name
        self.value_one = value_one
        self.value_two = value_two
        self.value_three = value_three
        self.value_four = value_four
        self.value_five = value_five
        self.value_six = value_six
        self.value_seven = value_seven



# create tables
Base.metadata.create_all(engine)