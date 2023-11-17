# %%
import pandas as pd
import os

from dotenv import load_dotenv
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy.orm import Session

from db_utils.database import get_db
from db_utils import schemas, models
from worker import *

# %%

# create path to db_utils (parent directory of this file, the db_utils/.env)
dotenv_path = os.path.join(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.pardir)
    ), 'db_utils', '.env')
load_dotenv(dotenv_path)


router = APIRouter(
    prefix="/v1/admin",
    tags=['Data'],
    dependencies=[Depends(get_db)]
)


@router.get('/dataStructure', status_code=200, response_model=schemas.Admin)
def get_data_structure(db: Session = Depends(get_db)):
    # create a dictionary that conforms to the admin schema from schemas.py
    data_structure = {
        'study_metadata_table': {
            'db_schema': 'public',
            'table': 'studies',
            # create fields, a list of dictionaries matching the StudyBase schema from schemas.py
            'fields': [{'bioproject_uid': 'integer'},
                       {"accession_number": "character"},
                       {"title": "character"},
                       {"description": "character"},
                       {"organism": "character"},
                       {"condition": "character"},
                       {"submitted": "character"},
                       {"organization": "character"},
                       {"n_samples": "integer"},
                       {"data_type": "character"},
                       {"sourced_method": "character"},
                       {"sequencing_method": "character"},
                       {"strategy": "character"},
                       {"layout": "character"},
                       {"has_data": "integer"}]
        },
        'data_table': {
            'db_schema': 'public',
            'table': 'microbiome',
            # create fields, a list of dictionaries matching the Microbiome model in models.py
            'fields': [{'tax_id': 'integer'},
                       {'rank': 'character'},
                       {'name': 'character'},
                       {'total_count': 'integer'},
                       {'self_count': 'integer'},
                       {'ilevel': 'integer'},
                       {'ileft': 'integer'},
                       {'iright': 'integer'},
                       {'bioproject_uid': 'integer'},
                       {'sra_acc': 'character'}
                       ]
        },
        'shared_key': 'bioproject_uid'
    }
    return JSONResponse(data_structure, status_code=200)

# create a route that returns a InputCollection schema with two Test schema objects inside


@router.get('/inputs', status_code=200, response_model=schemas.InputCollection)
def get_test():
    input_collection = {
        'inputs': [
            {
                'function': "checkboxInput",
                'searchField': "has_data",
                'split_download': False,
                'args': {
                    'label': "Has data?",
                    'checked': True
                }
            },
            {
                'function': "textInput",
                'searchField': "search_string",
                'split_download': False,
                'args': {
                    'label': "Search terms",
                    'placeholderText': "Enter one or more search terms"
                }
            },
            {
                'function': "selectInput",
                'searchField': "organism",
                'split_download': True,
                'args': {
                    'label': "Organism",
                    'options': [],
                    'source': 'https://respire-microbiome.dartmouth.edu/v1/studies/organisms'
                }
            },
            {
                'function': "numberInput",
                'searchField': "n_samples",
                'split_download': False,
                'args': {
                    'label': "Minimum Samples",
                    'defaultValue': 50
                }
            }
        ]
    }
    return JSONResponse(input_collection, status_code=200)
