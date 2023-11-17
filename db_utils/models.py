from sqlalchemy import Column, Integer, String

from .database import Base

class Study(Base):

    __tablename__ = "studies"

    bioproject_uid = Column(Integer, primary_key = True, unique = True, index = True)
    accession_number = Column(String)
    title = Column(String, default="")
    description = Column(String, default="")
    organism = Column(String, default="")
    condition = Column(String, default="")
    submitted = Column(String, default=None)
    organization = Column(String, default=None)
    n_samples = Column(Integer)
    data_type = Column(String, default=None)
    sourced_method = Column(String, default=None)
    sequencing_method = Column(String, default=None)
    strategy = Column(String, default=None)
    layout = Column(String, default=None)
    has_data = Column(Integer)


class Microbiome(Base):

    __tablename__ = "microbiome"

    bioproject_uid = Column(Integer, primary_key = True, index = True)
    sra_acc = Column(String, primary_key = True, index = True)
    tax_id = Column(Integer, primary_key = True, index = True)
    rank = Column(String)
    name = Column(String)
    total_count = Column(Integer)
    self_count = Column(Integer)
    ilevel = Column(Integer)
    ileft = Column(Integer)
    iright = Column(Integer)
    

