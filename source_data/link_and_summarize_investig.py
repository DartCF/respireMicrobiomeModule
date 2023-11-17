# %%
from Bio import Entrez
from Bio.Entrez import esearch, efetch, esummary
import xml.etree.ElementTree as ET
import pandas as pd
from retry import retry
from functions import extract_var, get_links, extract_keys, get_ncbi_summary
from microbiome_struct import microbiome_struct
import xmltodict
# from microbiome_struct import microbiome_struct
# %%
Entrez.email = 'matthew.rogers@dartmouth.edu'
bioproject_uid = '935808'
# %%
fetch_handle = efetch(db='bioproject', id=[bioproject_uid])

results = fetch_handle.read()
fetch_handle.close()
xml = ET.XML(results)

names = [e['name'] for e in microbiome_struct['vars']]
result_list = xml.findall(microbiome_struct['root'])

# pre-allocate space for results -- avoiding nested list comprehension
rows = [None]*len(result_list)

# for each result, extract each needed variable and
for i in range(len(result_list)):
    rows[i] = pd.DataFrame(
        [[extract_var(result_list[i], v) for v in microbiome_struct['vars']]], columns=names
    )

study_metadata = pd.concat(rows)


# project_dict = xmltodict.parse(results)

links = get_links(db_from='bioproject', db_to='sra', study_id=bioproject_uid)
# %%
search_handle = esearch(db='sra', term='PRJNA935808')
res = search_handle.read()
search_xml = ET.XML(res)
search_dict = xmltodict.parse(res)
# %%
# UID -> BioProject Accession
# BioProject Accession -> SRA Accessions
links = get_links(db_from='bioproject', db_to='sra', study_id='590873')

sra_ids = [e['Id'] for e in links['eLinkResult']['LinkSet']['LinkSetDb'][0]['Link']]

summary_handle = esummary(db='sra', id=",".join(sra_ids))
summary_res = summary_handle.read()
# convert to xml and then dict
summary_xml = ET.XML(summary_res)
summary_dict = xmltodict.parse(summary_res)
sra_accs = [xmltodict.parse(e['Item'][1]['#text'])['Run']['@acc'] for e in summary_dict['eSummaryResult']['DocSum']]

# create a dataframe with two columns, one for the bioproject uid and one for the sra accession
df = pd.DataFrame({'bioproject_uid': [bioproject_uid]*len(sra_accs), 'sra_acc': sra_accs})

#%%
summary_handle = esummary(db='sra', id=['26661253'])
summary_res = summary_handle.read()
# convert to xml and then dict
summary_xml = ET.XML(summary_res)
summary_dict = xmltodict.parse(summary_res)

sra_acc = xmltodict.parse(summary_dict['eSummaryResult']['DocSum']['Item'][1]['#text'])['Run']['@acc']
# %%
# extract the Run acc from the summary dict
summary_dict['eSummaryResult']['DocSum']
# %%
search_handle = esearch(db='biosample', term='935808')
res = search_handle.read()
search_xml = ET.XML(res)
search_dict = xmltodict.parse(res)
# %%
links = get_links(db_from='bioproject', db_to='sra', study_id='590873')

sra_ids = [e['Id'] for e in links['eLinkResult']['LinkSet']['LinkSetDb'][0]['Link']]

# summary_handle = esummary(db='biosample', id=biosample_ids[0])
# summary_res = summary_handle.read()
# # convert to xml and then dict
# summary_xml = ET.XML(summary_res)
# summary_dict = xmltodict.parse(summary_res)
# %%
# summary_dict1 = summary_dict
# %%
sd_xml = ET.parse(summary_dict['eSummaryResult']['DocumentSummarySet']['DocumentSummary']['SampleData'])
# %%
xmltodict.parse(sd_xml)
# %%
lstKey = []
lstValue = []
for p in summary_xml.iter():
    print(p.tag, p.text)
    # lstKey.append(summary_xml.getpath(p).replace("/",".")[1:])
    # lstValue.append(p.text)

# df = pd.DataFrame({'key' : lstKey, 'value' : lstValue})
# df.sort_values('key')
# %%

# %%
tstdct = xmltodict.parse(summary_dict['eSummaryResult']['DocumentSummarySet']['DocumentSummary']['SampleData'])
tstdct2 = xmltodict.parse(summary_dict1['eSummaryResult']['DocumentSummarySet']['DocumentSummary']['SampleData'])
# %%

#%% join 