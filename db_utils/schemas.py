from typing import Optional, List, Dict
from pydantic import BaseModel
from typing_extensions import TypedDict

# study schemata
class StudyBase(BaseModel):
    bioproject_uid: int
    accession_number: str
    title: str
    description: str
    organism:  str
    condition: Optional[str]
    submitted: Optional[str]
    organization: Optional[str]
    n_samples: int
    data_type: Optional[str]
    sourced_method: Optional[str]
    sequencing_method: Optional[str]
    strategy: Optional[str]
    layout: Optional[str]
    has_data: int

class StudyCreate(StudyBase):
    pass

class Study(StudyBase):
    bioproject_uid: int
    class Config:
        orm_mode = True

# search schema

class Search(BaseModel):
    search_string: str
    n_samples: int
    organism: str
    has_data: int


# administrative schemata

class MetadataTable(TypedDict):
    db_schema: str
    table: str
    fields: List[Dict[str, str]]

class DataTable(TypedDict):
    db_schema: str
    table: str
    fields: List[Dict[str, str]]

class Admin(BaseModel):
    metadata_table: MetadataTable
    data_table: DataTable
    shared_key: str

    
class InputCollection(BaseModel):
    test_cases: List[dict]

class SearchResult(BaseModel):
    accession_number: str
    title: str
    description: str
    n_samples: int
    has_data: int