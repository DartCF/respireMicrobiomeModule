# %%
import pandas as pd
import tempfile
import zipfile
import boto3
import os
import re

from dotenv import load_dotenv
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy import insert

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
    prefix="/v1/data",
    tags=['Data'],
    dependencies=[Depends(get_db)]
)




@router.post("/download", response_class=FileResponse)
def download_data_file(bioproject_uids: List[int], db: Session = Depends(get_db)):
    """Download selected studies

    Args:\n
        study_accessions (list[str]): A list of study IDs
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:\n
        FileResponse: A ZIP file containing data for selected studies
    """
    archive_time = datetime.now()

    data_query = db.query(
        models.Microbiome.bioproject_uid,
        models.Microbiome.sra_acc,
        models.Microbiome.tax_id,
        models.Microbiome.rank,
        models.Microbiome.name,
        models.Microbiome.total_count,
        models.Microbiome.self_count,
        models.Microbiome.ilevel,
        models.Microbiome.ileft,
        models.Microbiome.iright
    ).filter(
        models.Microbiome.bioproject_uid.in_(bioproject_uids)
    )

    res_df = pd.read_sql(
        data_query.statement, db.bind
    )

    # stop if empty
    if res_df.shape[0] == 0:
        raise HTTPException(
            status_code=404, detail="Studies specified do not have data available for download")
    
    # create a dataframe called metadata_df that contain the unique values of sra_acc from res_df
    metadata_df = res_df[['bioproject_uid', 'sra_acc']].drop_duplicates()
    # create a new column called metadata_link that interpolates sra_acc
    # link format is https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc={sra_acc}&display=metadata
    metadata_df['metadata_link'] = metadata_df['sra_acc'].apply(lambda x: f"https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc={x}&display=metadata")

    outdir = os.path.join(tempfile.gettempdir(), 'respire_data_download')

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    zip_fp = os.path.join(outdir, 'respire_data_download.zip')
    metadata_fp = os.path.join(outdir, "metadata.csv")
    data_fp = os.path.join(outdir, "data_compendium.csv")
    readme_fp = os.path.join(outdir, "readme.txt")

    res_df.to_csv(data_fp, index=False)
    metadata_df.to_csv(metadata_fp, index=False)

    with open(readme_fp, 'wt') as f:
        f.writelines(line + "\n" for line in [f"Downloaded on {archive_time.strftime('%m-%d-%Y at %H:%M:%S')}",
                                              "Includes data from the following studies:", "  " + "\n  ".join([str(id) for id in bioproject_uids])])

    file_list = [metadata_fp, data_fp, readme_fp]

    with zipfile.ZipFile(zip_fp, 'w') as zip:
        for file in file_list:
            zip.write(file,
                      compress_type=zipfile.ZIP_DEFLATED,
                      arcname=f"respire_microbiome_data_download_{archive_time.strftime('%Y%m%d_%H_%M_%S')}/{os.path.basename(file)}")

    headers = {'Content-Disposition': f'attachment; filename="respire_microbiome_data{archive_time.strftime("%Y%m%d_%H_%M_%S")}_download.zip"',
               'Accept': 'application/zip, application/octet-stream '}

    return FileResponse(zip_fp, headers=headers)
