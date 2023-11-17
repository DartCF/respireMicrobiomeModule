from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from . import models

# return results from front end search


def search_studies(db: Session,
                   search_string: str,
                   n_samples: int,
                   organism: str,
                   has_data: int):
    return db.query(
        models.Study.bioproject_uid.label('accession_number'),
        models.Study.title,
        models.Study.description,
        models.Study.n_samples,
        models.Study.has_data
    ).filter(
        models.Study.description.ilike(f"%{search_string}%"),
        models.Study.n_samples >= n_samples,
        models.Study.organism == organism,
        models.Study.has_data == has_data
    ).all()


# def add_studies(db: Session, studies: List[schemas.StudyCreate]):
#     '''
#     Add one or more studies to the study metadata
#     '''
#     for study in studies:
#         s = models.Study(**study.dict())
#         db.add(s)
#     db.commit()
#     return [s.study_id for s in studies]


def list_hosts(db: Session, has_data: int = 1):
    '''
    Get a list of the available organisms in the database
    '''
    stmt = select(
        models.Study.host.distinct()
    ).filter(
        models.Study.has_data == has_data
    ).order_by(
        models.Study.host
    )

    res = db.execute(stmt).all()
    
    return [str(i[0]) for i in res]


def list_methods(db: Session, has_data: int = 1):
    '''
    Get a list of the available organisms in the database
    '''
    stmt = select(
        models.Study.method.distinct()
    ).filter(
        models.Study.has_data == has_data
    ).order_by(
        models.Study.method
    )

    res = db.execute(stmt).all()

    return [str(i[0]) for i in res]



def list_organisms(db: Session):
    '''
    Get a list of the available organisms in the database
    '''
    stmt = select(
        models.Study.organism.distinct()
    ).order_by(
        models.Study.organism
    )

    res = db.execute(stmt).all()

    return [str(i[0]) for i in res]
